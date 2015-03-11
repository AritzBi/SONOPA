__author__ = 'AritzBi'
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey,DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import csv
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import ConfigParser
import json
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker,relationship
config = ConfigParser.ConfigParser()
config.read('config.cfg')
period=config.getfloat('Rules','period')
json_period=config.getfloat('Rules','json_period')
json_data=open("houseConfiguration.json")
houseConfiguration=json.load(json_data)
json_data.close()
Base = declarative_base()

class Location(Base):
    __tablename__ = 'Location'
    """Represents the location of a Sensor in the system"""
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    sensors = relationship('Sensor', backref='located_in', lazy='dynamic')


class Sensor(Base):
    __tablename__ = 'Sensor'
    """Represents a sensor in the system"""
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    sensorRef = Column(String(64))
    type = Column(String(64))
    last_alive = Column(DateTime, default=datetime.now())
    location = Column(Integer, ForeignKey('location.id'))
    events = relationship('Event', backref='fired_by', lazy='dynamic')


class Event(Base):
    __tablename__ = 'Event'
    """Represents a sensor fired event"""
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    sensor = Column(Integer, ForeignKey('sensor.id'))
    #sensorRef = db.Column(db.Integer, db.ForeignKey('sensor.sensorRef'))
    value = Column(Text)

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
	engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
	Session = sessionmaker()
	Session.configure(bind=engine)
	session = Session()
	print formatedData