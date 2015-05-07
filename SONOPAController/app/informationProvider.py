from datetime import datetime,timedelta
import MySQLdb
from config import DB, DB_USER,DB_PASS,MAXPEOPLE_WEIGHT,SNINTERACTIONS_WEIGHT
import json
import random
from snRequester import getNumberActivities
json_data=open("houseConfiguration.json")
houseConfiguration=json.load(json_data)
json_data.close()

def concurrentDifferentRooms(values):
	concurrentActivations=[]
	lastTimeStamp=0
	counter=1
	biggestCounter=1
	for value in values:
		if(lastTimeStamp+1>=value[0]) and isDifferentPlace(concurrentActivations,value[1]):
			counter=counter+1
			concurrentActivations.append(value)
			#if(counter == 4):
				#print concurrentActivations
			if counter > biggestCounter:
				print concurrentActivations
				biggestCounter=counter
		else:
			counter=1
			concurrentActivations=[]
			concurrentActivations.append(value)
			lastTimeStamp=value[0]
	return biggestCounter

def calculate_concurrent(values):
	lastTimeStamp=0
	counter=1
	biggestCounter=1
	for value in values:
		if(lastTimeStamp+2>=value[0]):
			counter=counter+1
			if counter > biggestCounter:
				biggestCounter=counter
		else:
			counter=1
		lastTimeStamp=value[0]
	return biggestCounter
def isDifferentPlace(values, place):
	adjacentRooms=houseConfiguration[place]["adjacent"]
	for value in values:
		if value[1]==place:
			return False
	for value in values:
		for adjacentRoom in adjacentRooms:
			if value[1]==adjacentRoom:
				return False
	return True
def calculateRoomChanges(values):
	numRoomChanges=0
	lastRoom=values[0][1]
	adjacentRooms=houseConfiguration[lastRoom]["adjacent"]
	noAdjacentRooms=houseConfiguration[lastRoom]["noAdjacent"]
	adjacent=False
	for value in values:
		if(lastRoom!=value[1]):
			for adjacentRoom in adjacentRooms:
				if value[1]==adjacentRoom:
					numRoomChanges=numRoomChanges+1	
					adjacent=True	
					break
			if not adjacent:
				for noAdjacentRoom in noAdjacentRooms:
					if(value[1]==noAdjacentRoom['room']):
						numRoomChanges=numRoomChanges+noAdjacentRoom['distance']
						break
		lastRoom=value[1]
		adjacent=False
	return numRoomChanges
def calculate_room(values):
	roomMap= {}
	for value in values:
		roomMap[value[1]]=0
	for value in values:
		roomMap[value[1]]=roomMap[value[1]]+1
	biggestValue=0
	mostFrecuentActivation=""
	secondBiggestValue=0
	secondMostFrecuentActivation=""
	for key in roomMap:
		if roomMap[key]>biggestValue:
			secondMostFrecuentActivation=mostFrecuentActivation
			secondBiggestValue=biggestValue
			mostFrecuentActivation=key
			biggestValue=roomMap[key]
		elif roomMap[key]>secondBiggestValue:
			secondMostFrecuentActivation=key
			secondBiggestValue=roomMap[key]
	return [[mostFrecuentActivation,biggestValue], [secondMostFrecuentActivation,secondBiggestValue]]
def occupation_level(values):
	rooms={}
	lastActivation=values[0]
	total=0
	for value in values:
		rooms[value[1]]=0
	for value in values:
		rooms[value[1]]=rooms[value[1]]+1
		total=total+1
		if value[1]==lastActivation[1]:
			minutes=(value[0]-lastActivation[0])/60
			if minutes>2:
				total=total+minutes
				rooms[value[1]]=rooms[value[1]]+minutes
		lastActivation=value
	for key in rooms:
		rooms[key]="%.2f" %(rooms[key]*100/float(total))
	return rooms
#Mode 1=day Mode 2=hour
def getDataFromDB(date,mode=1):
	nextday=0
	if(mode == 1):
		nextday = date + timedelta(days = 1)
		date=date.strftime('%Y-%m-%d')
		nextday=nextday.strftime('%Y-%m-%d')
	if(mode == 2):
		nextday = date + timedelta(hours = 1)
		date=date.strftime('%Y-%m-%d %H:%M:%S')
		nextday=nextday.strftime('%Y-%m-%d %H:%M:%S')
	conn =  MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS,db=DB)
	cursor = conn.cursor()
	SQLSelect="SELECT UNIX_TIMESTAMP(e.timestamp),l.name FROM location l, sensor s, event e WHERE l.id=s.location and s.id=e.sensor and e.timestamp >= %s and e.timestamp < %s order by timestamp asc;"
	cursor.execute(SQLSelect,(date,nextday))
	conn.commit()
	return cursor.fetchall()

"""Retrieves the activeness in a precise day"""
def getActiveness(date,mode):
	data=getDataFromDB(date,mode)
	if len(data)==0:
		return 0
	return calculateRoomChanges(data)
"""Retrieves the socialization level in a precise day"""
def getSocializationLevel(date,mode):
	#TODO: query the social network's API in order to get the number of interactions
	interactions_sn=getNumberActivities(1)
	data=getDataFromDB(date,mode)
	if len(data)==0:
		return 0
	max_people=concurrentDifferentRooms(data)
	return MAXPEOPLE_WEIGHT*max_people+SNINTERACTIONS_WEIGHT*interactions_sn
"""Retrieves the occupation level of each of the rooms in a precise day"""
def getOccupationLevel(date,mode):
	data=getDataFromDB(date,mode)
	if len(data)==0:
		return 0
	return occupation_level(data)
"""Retrieves the maximum number of people in the house in a precise day"""
def getPresence(date,mode):
	data=getDataFromDB(date,mode)
	if len(data)==0:
		return 0
	return concurrentDifferentRooms(data)

