import json
import requests
from collections import OrderedDict
from urllib import urlencode
configuration_file = './configuration/config.json'
base='http://84.200.25.110/sonopa/api/'
sn_key=None
with open(configuration_file, 'r') as f:
	global sn_key
	config = json.load(f)
	sn_key=config['sn_api']
def getNumberActivities(userId):
	url=base+'cust/activitycount/?'+sn_key+"=json"
	params = OrderedDict([('UID', userId)])
	r=requests.get(url, params=urlencode(params))
	print r.json()

def getActivities(userId):
	url=base+'BuddyPressRead/activity_get_activities/?'+sn_key+'=json'
	params = OrderedDict([('UID', userId)])
	r=requests.get(url, params=urlencode(params))
	print r.json()
def sendRecommendation(userId, message):
	url=base+'cust/recommendation/?'+sn_key+'=json'
	params = OrderedDict([('UID', userId),('recommendation', message)])
	r=requests.get(url, params=urlencode(params))
	print r.json()
def sendSocializationLevel(userId, socialisation):
	url=base+'cust/socializationLevel/?'+sn_key+"=json"
	params = OrderedDict([('UID', userId),('socialization',socialisation)])
	r=requests.get(url, params=urlencode(params))
	print r.json()
def sendActiveness(userId, activeness):
	url=base+'cust/activeness/?'+sn_key+"=json"
	params = OrderedDict([('UID', userId),('activeness',activeness)])
	r=requests.get(url, params=urlencode(params))
	print r.json()
def sendOccupationLevel(userId, occupation, location):
	url=base+'cust/occupationLevel/?'+sn_key+"=json"
	params = OrderedDict([('UID', userId),('occupation',occupation),('location',location)])
	r=requests.get(url, params=urlencode(params))
	print r.json()
