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

import json
import requests
from collections import OrderedDict
from urllib import urlencode
from config import UID, sn_key, sn_url
from app import app
from utils import dict_to_string


#Gets the absolute number of activities of a user so far
def getNumberActivities():
    url = sn_url+'cust/activitycount/?'+sn_key+"=json"
    params = OrderedDict([('UID', UID)])
    r = requests.get(url, params=urlencode(params))
    message = r.json()['message']
    id_index = message.index('is ')
    return int(message[id_index+3:])


#Gets a list of activities of a user
def getActivities():
    url = sn_url+'BuddyPressRead/activity_get_activities/?'+sn_key+'=json'
    params = OrderedDict([('UID', UID)])
    r = requests.get(url, params=urlencode(params))
    print r.json()


#Sends a reccomendation for a user to the social network
def sendRecommendation(message):
    url = sn_url+'cust/recommendation/?'+sn_key+'=json'
    params = OrderedDict([('UID', UID), ('recommendation', message)])
    r = requests.get(url, params=urlencode(params))
    print r.json()


#Sends the socialization level of a user to the SN
def sendSocializationLevel(socialisation):
    url = sn_url+'cust/socializationLevel/?'+sn_key+"=json"
    params = OrderedDict([('UID', UID), ('socialization', socialisation)])
    r = requests.get(url, params=urlencode(params))
    #print r.json()
    app.logger.info("The response from the social network is: " + str(r.json()))


#Sends the activeness of a user to the SN
def sendActiveness(activeness):
    url = sn_url+'cust/activeness/?'+sn_key+"=json"
    params = OrderedDict([('UID', UID), ('activeness', activeness)])
    r = requests.get(url, params=urlencode(params))
    app.logger.info("The response from the social network is: " + str(r.json()))


#Seds the statistics about the diary occupation level for a user of eachf od the rooms
def sendOccupationLevel(occupation, location):
    url = sn_url+'cust/occupationLevel/?'+sn_key+"=json"
    params = OrderedDict([('UID', UID), ('occupation', occupation), ('location', location)])
    r = requests.get(url, params=urlencode(params))
    print r.json()


def getConnections(username):
    url = sn_url+'/BuddyPressRead/friends_get_friends/?'+sn_key+"=json"
    params = OrderedDict([('username', username)])
    r = requests.get(url, params=urlencode(params))
    html = r.json()
    try:
        friends = html['friends']
    except:
        friends = []
    friendNames = []
    for i in friends:
        friendNames.append(friends[i]['username'])
    return friendNames


def getProfile(username):
    url = sn_url+'/BuddyPressRead/profile_get_profile/?'+sn_key+"=json"
    params = OrderedDict([('username', username)])
    r = requests.get(url, params=urlencode(params))
    html = r.json()
    basicInfo = html['profilefields']['Base']
    try:
        activeness = html['profilefields']['Base']['Activeness']
        activeness = activeness.split("href")[1].split(">")[1].split("<")[0]
    except:
        activeness = 0
    try:
        socialization = html['profilefields']['Base']['Socialization']
        socialization = socialization.split("href")[1].split(">")[1].split("<")[0]
    except:
        socialization = 0
    try:
        location = html['profilefields']['Base']['Home town']
        location = location.split("href")[1].split(">")[1].split("<")[0]
    except:
        location = ""
    try:
        moreInformation = html['profilefields']['That\'s me']
        try:
            hobbies = moreInformation['Hobbies']
        except:
            hobbies = []
        try:
            moreHobbies = moreInformation['More hobbies']
        except:
            moreHobbies = []
        if moreHobbies:
            totalHobbies = hobbies+','+moreHobbies
        else:
            totalHobbies = hobbies
        finalHobbies = []
        if totalHobbies:
            tokens = totalHobbies.split(',')
            for token in tokens:
                finalHobbies.append(token.split("href")[1].split(">")[1].split("<")[0])
    except:
        finalHobbies = []
    friends = getConnections(username)
    profile = {
            'socialization': int(socialization),
            'activeness': int(activeness),
            'hobbies': finalHobbies,
            'connections': friends,
            'location': location.lower()}
    return profile


def getUsers():
    url = sn_url+'/cust/getallusers/?'+sn_key+"=json"
    r = requests.get(url)
    users = r.json()['users']
    users = users.split(',')
    users[0:2] = []
    users[len(users)-1:] = []
    i = 0
    usersFinal = []
    while i < len(users):
        usersFinal.append({'username': users[i], 'id': int(users[i+1])})
        i = i+2
    return usersFinal
