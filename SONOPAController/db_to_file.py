import sys
from informationProvider import *
import	json
#Mode 1 the interval is a day, and mode 2 is an hour.
mode=int(sys.argv[1])
startDate=datetime(2014, 8, 12)
endDate=datetime(2014,10,13)
array=[]
if mode ==1:
	interval=timedelta(days = 1)
elif mode  ==2:
	interval=timedelta(hours = 1)
while startDate < endDate:
	data={}
	data['date']=str(startDate)
	data['activeness']= getActiveness(startDate,mode)
	data['socialization']=getSocializationLevel(startDate,mode)
	data['occupation_level']=getOccupationLevel(startDate,mode)
	data['presence']=getPresence(startDate,mode)
	startDate=startDate+interval
	array.append(data)
with open('data_hourly.json','a') as thefile:
	thefile.write(json.dumps(array))
