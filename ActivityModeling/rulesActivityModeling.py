__author__ = 'AritzBi'
import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import pandas as pd 
import numpy as np
from pandas import Series, DataFrame, Panel
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
		sec_epoch_utc = calendar.timegm(tt) * 1000
		dataArray.append(sec_epoch_utc)
		dataArray.append(location)
		formatedData.append(dataArray)
	data=np.array(formatedData)
	dates = pd.date_range('1950-01', '2013-03', freq='M')
	print data.shape
		
