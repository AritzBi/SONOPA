import json
from datetime import datetime,timedelta
import MySQLdb
from config import DB, DB_USER,DB_PASS
import time
#Returns the reading of the sensors in a time interval
def getTimeIntervalBySensor(sensor_id, start_time, end_time):
    conn =  MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS,db=DB)
    cursor = conn.cursor()
    #SQLSelect="SELECT UNIX_TIMESTAMP(e.timestamp),l.name FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and s.id=%s and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    SQLSelect="SELECT count(e.timestamp) FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and s.id=%s and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    cursor.execute(SQLSelect,  (sensor_id,start_time,end_time))
    conn.commit()
    return cursor.fetchall()
def getTimeInterval(start_time,end_time):
    conn =  MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS,db=DB)
    cursor = conn.cursor()
    SQLSelect="SELECT count(e.timestamp) FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
    cursor.execute(SQLSelect,  (start_time,end_time))
    conn.commit()
    return cursor.fetchall()
def insertState(state):
    conn =  MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS,db=DB)
    cursor=conn.cursor()
    select_state="SELECT ID FROM ACTIVITY_MODEL WHERE NAME=%s"
    cursor.execute(select_state, (state,))
    ids=cursor.fetchall()
    id=ids[0][0]
    print id
    now=datetime.now()
    insert_state="INSERT INTO ACTIVITY (activity_model_id,timestamp) VALUES (%s,%s);"
    cursor.execute(insert_state,(int(id),now))
    conn.commit()

def calculatePercentaje(data, data_total, active,percentaje):
    print data_total
    print data
    print active
    if active and ((data/data_total)*100)>percentaje:
         return True
    elif not active and ((data/data_total)*100)<percentaje:
        return True
    return False

#stamp= time.time()
#today=datetime.fromtimestamp(stamp)
now=datetime(2014,8,13,17,11,18)
with open('./rules.json') as rules_file:
    rules_json=json.load(rules_file)
    rules=[]
    for rule_json in rules_json:
        for condition in rule_json[0]:
            if condition['condition_type']=="Time interval":
                start_time=now.replace(hour=int(condition['start_time'].split(":")[0]),minute=int(condition['start_time'].split(":")[1]),second=0)
                end_time=now.replace(hour=int(condition['end_time'].split(":")[0]),minute=int(condition['end_time'].split(":")[1]),second=0)
                #now=datetime.now()
                if(start_time<now<end_time):
                    half_hour=now-timedelta(minutes=30)
                    data=getTimeIntervalBySensor(condition['sensor_id'],half_hour,now)
                    data_total=getTimeInterval(half_hour,now)
                    continue_loop=calculatePercentaje(data[0][0],data_total[0][0],condition['active'],70)
                else:
                    continue_loop=False
                if not continue_loop:
                    print "no"
                    print condition
                    break;
        if continue_loop:
            for consequence in rule_json[1]:
                print consequence
                if consequence['consequence_type']=='State':
                    insertState(consequence['state'])
                elif consequence['consequence_type']=='Message':   		
                    print "Message: "+consequence['message']