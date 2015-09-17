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

import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import ConfigParser
import json
#from config import DB, DB_USER,DB_PASS
import MySQLdb
config = ConfigParser.ConfigParser()
config.read('config.cfg')
#period=config.getfloat('Rules','period')
#json_period=config.getfloat('Rules','json_period')
#json_data=open("houseConfiguration.json")
#houseConfiguration=json.load(json_data)
#json_data.close()
lastID = "SELECT LAST_INSERT_ID();"

conn = MySQLdb.connect(host="localhost", user="sonopa", passwd="sonopa", db="sonopa")

cursor = conn.cursor()
with open('sorted_2.csv', 'rb') as csvfile:
    formatedData = []
    i = 0
    data = csv.reader(csvfile, delimiter=' ')
    numberOfActivations = 0
    for row in data:
        date = row[0].split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        time = row[1].split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = (time[2].split(','))[0]
        location = (time[2].split(','))[1]
        second = int((second.split('.', 2))[0])
        dataArray = []
        completeDate = datetime(year, month, day, hour, minute, second)
        tt = datetime.timetuple(completeDate)
        sec_epoch_utc = calendar.timegm(tt)
        dataArray.append(int(sec_epoch_utc))
        dataArray.append(location)
        formatedData.append(dataArray)
        numberOfActivations = numberOfActivations + 1
    for data in formatedData:
        SQLSelect = "SELECT id FROM location WHERE NAME=%s;"
        cursor.execute(SQLSelect, (data[1],))
        if cursor.rowcount == 0:
            SQLInsert = "INSERT INTO location (name) VALUES (%s);"
            cursor.execute(SQLInsert, (data[1],))
            cursor.execute(lastID)
            location_id = cursor.fetchone()[0]
            print location_id
            SQLInsert = "INSERT INTO sensor (name,location, type) VALUES (%s,%s,%s);"
            cursor.execute(SQLInsert, ("PIR sensor", location_id, "PIR sensor"))
            cursor.execute(lastID)
            sensor_id = cursor.fetchone()[0]
        else:
            SQLSelect = "SELECT s.id FROM sensor s, location l WHERE l.name=%s and l.id=s.location;"
            cursor.execute(SQLSelect, (data[1],))
            sensor_id = cursor.fetchone()[0]
        SQLInsert = "INSERT INTO event (timestamp,sensor, value) VALUES (%s,%s,%s);"
        cursor.execute(SQLInsert, (datetime.fromtimestamp(data[0]), sensor_id, '{"status":"activated"}'))
conn.commit()
