__author__ = 'AritzBi'
import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import ConfigParser
import json
config = ConfigParser.ConfigParser()
config.read('config.cfg')
period=config.getfloat('Rules','period')
json_period=config.getfloat('Rules','json_period')
json_data=open("houseConfiguration.json")
houseConfiguration=json.load(json_data)
json_data.close()



with open('SensorDataSurrey.csv','rb') as csvfile:
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