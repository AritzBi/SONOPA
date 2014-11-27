__author__ = 'AritzBi'
"""t=datetime.fromtimestamp(float(data[0][0]))
start=t.strftime('%Y-%m')"""
import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
with open('SensorDataSurrey.csv','rb') as csvfile:
	formatedData=[]
	i=0;
	data=csv.reader(csvfile,delimiter=' ')
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

	upperLimit=formatedData[0][0]+300
	index=0
	intervalsArray=[]
	while(index<len(formatedData)):
		interval=[]
		intervalsArray.append(interval)
		limit=False
		while(not limit and index<len(formatedData)):
			data=formatedData[index]
			if(upperLimit<data[0]):
				upperLimit=formatedData[index][0]+300
				limit=True
			else:
				interval.append(data)	
				index=index+1
	print intervalsArray[0]



		
