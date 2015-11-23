__author__ = 'AritzBi'
import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import ConfigParser
import json
import MySQLdb

config = ConfigParser.ConfigParser()
config.read('config.cfg')
filename = "surrey.csv"
lastID="SELECT LAST_INSERT_ID();"

print "Loading..."
conn =  MySQLdb.connect(host="localhost", user="sonopa", passwd="sonopa",db="sonopa")
cursor = conn.cursor()
try: 
	with open(filename,'rb') as csvfile:
		formatedData=[]
		i=0;
		data=csv.reader(csvfile,delimiter=' ')
		numberOfActivations=0
		for row in data:
			date=row[0].split('-' );
			year=int(date[0])
			month=int(date[1])
			day=int(date[2])
			time=row[1].split(':')
			hour=int(time[0])
			minute=int(time[1])
			second=(time[2].split(','))[0]
			location=(time[2].split(','))[1]
			second=int((second.split('.',2))[0])
			dataArray=[]
			completeDate=datetime(year,month,day,hour,minute,second)
			tt = datetime.timetuple(completeDate)
			sec_epoch_utc = calendar.timegm(tt)
			dataArray.append(int(sec_epoch_utc))
			dataArray.append(location)
			formatedData.append(dataArray)
			numberOfActivations=numberOfActivations +1
		for data in formatedData:
			SQLSelect="SELECT id FROM location WHERE NAME=%s;"
			cursor.execute(SQLSelect,(data[1],))
			if cursor.rowcount==0:
				SQLInsert="INSERT INTO location (name) VALUES (%s);"
				cursor.execute(SQLInsert, (data[1],))
				cursor.execute(lastID)	
				location_id=cursor.fetchone()[0]
				SQLInsert="INSERT INTO sensor (name,location, type) VALUES (%s,%s,%s);"
				cursor.execute(SQLInsert, ("PIR sensor",location_id,"PIR sensor"))
				cursor.execute(lastID)
				sensor_id=cursor.fetchone()[0]
			else:
				SQLSelect="SELECT s.id FROM sensor s, location l WHERE l.name=%s and l.id=s.location;"
				cursor.execute(SQLSelect,(data[1],))
				sensor_id=cursor.fetchone()[0]
			SQLInsert="INSERT INTO event (timestamp,sensor, value) VALUES (%s,%s,%s);"
			cursor.execute(SQLInsert,(datetime.fromtimestamp(data[0]),sensor_id,'{"status":"activated"}'))
except:
	print "The filename is incorrect or the file is not in the indicated folder"



conn.commit()
print "Finished"
