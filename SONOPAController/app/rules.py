"""
Copyright (c) 2015 Aritz Bilbao, Aitor Almeida
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
@author: "Aritz Bilbao, Aitor Almeida"
@contact: aritzbilbao@deusto.es, aitor.almeida@deusto.es
"""

import json
from datetime import datetime, timedelta
import MySQLdb
from config import DB, DB_USER, DB_PASS
import time
from utils.snRequester import sendRecommendation
from threading import Thread


#Returns the reading of the sensors in a time interval
def getTimeIntervalBySensor(sensor_id, start_time, end_time):
    conn = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS, db=DB)
    cursor = conn.cursor()
    #SQLSelect="SELECT UNIX_TIMESTAMP(e.timestamp),l.name FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and s.id=%s and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    SQLSelect = "SELECT count(e.timestamp) FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and s.id=%s and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    cursor.execute(SQLSelect,  (sensor_id, start_time, end_time))
    conn.commit()
    return cursor.fetchall()


def getTimeInterval(start_time, end_time):
    conn = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS, db=DB)
    cursor = conn.cursor()
    SQLSelect = "SELECT count(e.timestamp) FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    cursor.execute(SQLSelect,  (start_time, end_time))
    conn.commit()
    return cursor.fetchall()


def insertState(state):
    conn = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS, db=DB)
    cursor = conn.cursor()
    select_state = "SELECT ID FROM activity_model WHERE NAME=%s"
    cursor.execute(select_state, (state,))
    ids = cursor.fetchall()
    id = ids[0][0]
    now = datetime.now()
    insert_state = "INSERT INTO activity (activity_model_id,timestamp) VALUES (%s,%s);"
    cursor.execute(insert_state, (int(id), now))
    conn.commit()


def calculatePercentaje(data, data_total, active, percentaje):
    try:
        current_percent = ((float(data)/data_total)*100)
    except:
        return False
    if data_total == 0 and percentaje == 0:
        return False
    else:
        return True
    if active and current_percent > percentaje:
        return True
    elif not active and current_percent < percentaje:
        return True
    return False


class RuleThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.signal = True
        self.read_json = True

    def run(self):
        print "Starting the rules thread"
        while self.signal:
            time.sleep(1)
            if self.read_json == True:
                with open('./rules.json') as rules_file:
                    rules_json = json.load(rules_file)
                    self.read_json = False
            stamp = time.time()
            now = datetime.fromtimestamp(stamp)
            #now=datetime(2015,6,28,23,30,0)
            rules = []
            for rule_json in rules_json:
                for condition in rule_json[0]:
                    if condition['condition_type'] == "Time interval":
                        start_time = now.replace(hour=int(condition['start_time'].split(":")[0]), minute=int(condition['start_time'].split(":")[1]), second=0)
                        end_time = now.replace(hour=int(condition['end_time'].split(":")[0]), minute=int(condition['end_time'].split(":")[1]), second=0)
                        if end_time < start_time:
                            end_time = end_time + timedelta(hours=24)
                        now = datetime.now()
                        if(start_time < now < end_time):
                            continue_loop = True
                        else:
                            continue_loop = False
                        if not continue_loop:
                            #print "no"
                            #print condition
                            break
                if continue_loop:
                    for condition in rule_json[0]:
                        if condition['condition_type'] == "PIR rule":
                            checking_interval = now-timedelta(seconds=condition['check_interval'])
                            #print 'Checking interval',checking_interval
                            #print 'Last time checked',datetime.fromtimestamp(condition['last_checked'])
                            #print 'Difference ', datetime.fromtimestamp(condition['last_checked'])-checking_interval
                            #print 'Result',datetime.fromtimestamp(condition['last_checked'])-checking_interval > timedelta(seconds=condition['check_interval'])
                            if(condition['last_checked'] == 0 or datetime.fromtimestamp(condition['last_checked']) < checking_interval):
                                data_interval = now-timedelta(seconds=condition['data_interval'])
                                data = getTimeIntervalBySensor(condition['sensor_id'], data_interval, now)
                                data_total = getTimeInterval(data_interval, now)
                                continue_loop = calculatePercentaje(data[0][0], data_total[0][0], condition['active'], condition['percentage'])
                                #print 'Continue',continue_loop
                                #print 'Setting last_checked', datetime.fromtimestamp(stamp)
                                condition['last_checked'] = stamp
                            else:
                                continue_loop = False
                            if not continue_loop:
                                break

                    if continue_loop:
                        for consequence in rule_json[1]:
                            #print 'The conseuconsequence
                            if consequence['consequence_type'] == 'State':
                                insertState(consequence['state'])
                            elif consequence['consequence_type'] == 'Message':
                                sendRecommendation(consequence['message'])
                                #print "Message: "+consequence['message']
        print "Finishing the rules thread"
