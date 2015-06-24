__author__ = 'AritzBi'
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
lastID="SELECT LAST_INSERT_ID();"

conn =  MySQLdb.connect(host="localhost", user="sonopa", passwd="sonopa",db="sonopa")

cursor = conn.cursor()
SQLSelect="Select id from activity_model where NAME=%s;"
cursor.execute(SQLSelect,("Cook",))
if cursor.rowcount == 0:
	SQLINSERT="INSERT INTO activity_model (name) values(%s)";
	cursor.execute(SQLINSERT,("Wake",))
	cursor.execute(SQLINSERT,("Cook",))
	cursor.execute(SQLINSERT,("Relax",))
	cursor.execute(SQLINSERT,("Eat",))
	cursor.execute(SQLINSERT,("Sleep",))
else:
	print "The activity_model table is already filled"
with open('sorted_3.csv','rb') as csvfile:
	formatedData=[]
	i=0;
	data=csv.reader(csvfile)
	numberOfActivations=0
	for row in data:
		row_date = row[0].split(' ')
		date=row_date[0].split('-' );
		year=int(date[0])
		month=int(date[1])
		day=int(date[2])
		time=row_date[1].split(':')
		hour=int(time[0])
		minute=int(time[1])
		second=int(time[2])
		location=row[1]
		dataArray=[]
		completeDate=datetime(year,month,day,hour,minute,second)
		#tt = datetime.timetuple(completeDate)
		#sec_epoch_utc = calendar.timegm(tt)
		#dataArray.append(int(sec_epoch_utc))
		dataArray.append(completeDate)
		dataArray.append(location)
		formatedData.append(dataArray)
		numberOfActivations=numberOfActivations +1
	for data in formatedData:
		#print "Time",data[0]
		#print "Location",data[1]
		SQLSelect="SELECT id FROM location WHERE NAME=%s;"
		cursor.execute(SQLSelect,(data[1],))
		if cursor.rowcount==0:
			print "The location is not in the database"
		else:
			SQLSelect="SELECT s.id FROM sensor s, location l WHERE l.name=%s and l.id=s.location;"
			cursor.execute(SQLSelect,(data[1],))
			sensor_id=cursor.fetchone()[0]
			#print "From timestamp", datetime.fromtimestamp(data[0])
		SQLInsert="INSERT INTO event (timestamp,sensor, value) VALUES (%s,%s,%s);"
		cursor.execute(SQLInsert,(data[0],sensor_id,'{"status":"activated"}'))
conn.commit()
