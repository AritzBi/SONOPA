import sys
import argparse
import json
import requests
from datetime import datetime, timedelta, date, time
from informationProvider import *
import numpy as np
import config

from messages import get_message


"""
IPI recommendations module.

Generates recommendations based on information provided by the Sonopa Controller,
and posts them to the Sonopa Push UI.

refer to the IPIRecommendations class below to integrate this into the Sonopa
Controller itself.

"""



ltbath = 4.4480
ltsleep = 3.3397
lteat = 20.2830
ltactivity = 682
ltsocial = 171.6

htbath = 10.9440
htsleep = 12.3820
hteat = 37.8480
htactivity = 802
htsocial = 406




class PushUI():
    def __init__(self, url='http://localhost:5000', username='user', password='pass'):
        self.url = url
        self.username = username
        self.password = password

        self.session = requests.session()
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        self.user_id = '0'

    def post_message(self, title, description, date=None, startTime=None, endTime=None, topic=None, img=None):

        msg = {'title': title,
               'description' : description,
               'userId': self.user_id }

        if date:
            msg['date'] = date.strftime('%Y-%m-%d')

        if startTime:
            msg['startTime'] = startTime.strftime('%H:%M')

        if endTime:
            msg['endTime'] = endTime.strftime('%H:%M')

        if topic:
            msg['topic'] = topic

        if img:
            msg['img'] = img.decode('utf-8')

        r = self.session.post("%s/message.sms"%self.url, data=json.dumps(msg), headers=self.headers)

        return r.status_code == requests.codes.ok

def cal_low_threshold(counts, centers):
    #print 'Low : ', counts
    prob = 0
    bin = (centers[1] - centers[0])/2.0
    for i in range(0, len(counts)):
        prob = prob + counts[i]
        if(prob > config.prob_sens):
            return centers[i] - bin

def cal_high_threshold(counts, centers):
    #print 'High : ', counts
    prob = 0
    bin = (centers[1] - centers[0])/2.0
    for i in range(len(counts) - 1, -1, -1):
        prob = prob + counts[i]
        if(prob > config.prob_sens):
            return centers[i] + bin

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_thresholds(day):
    start_date = day - timedelta(days=config.num_days)
    end_date = day - timedelta(days=1)

    #print 'Start : ', start_date.strftime('%Y%m%d')
    #print 'End : ', end_date.strftime('%Y%m%d')

    eat_list = []
    sleep_list = []
    active_list = []
    bath_list = []
    total_days = 0

    for single_date in daterange(start_date, end_date):
        curactive = getActiveness(single_date)

        if(curactive < 0):
            continue

        active_list.append(curactive)

        curroom = getOccupationLevel(single_date)

        curkitchen = 0
        curdinning = 0
        curbath = 0
        curbed = 0
        if curroom != 0:
            if 'HS_Kitchen' in curroom:
                curkitchen = float(curroom['HS_Kitchen'])

            if 'HS_Dining_Room' in curroom:
                curdinning = float(curroom['HS_Dining_Room'])

            if 'HS_Bathroom' in curroom:
                curbath = float(curroom['HS_Bathroom'])

            if 'HS_Bedroom' in curroom:
                curbed = float(curroom['HS_Bedroom'])

        cureat = curdinning + curkitchen

        eat_list.append(cureat)
        sleep_list.append(curbed)
        bath_list.append(curbath)

        total_days = total_days + 1

    # computing threshold for eating activity
    [counts, centers] = np.histogram(eat_list)

    counts = counts*(1.0/total_days)

    hteat = cal_high_threshold(counts, centers)
    lteat = cal_low_threshold(counts, centers)

    #print 'Eat : ', lteat, '-', hteat

    # computing threshold for overall activity
    [counts, centers] = np.histogram(active_list)

    counts = counts*(1.0/total_days)

    htactivity = cal_high_threshold(counts, centers)
    ltactivity = cal_low_threshold(counts, centers)

    #print 'Activity : ', ltactivity, '-', htactivity

     # computing threshold for sleeping activity
    [counts, centers] = np.histogram(sleep_list)

    counts = counts*(1.0/total_days)

    htsleep = cal_high_threshold(counts, centers)
    ltsleep = cal_low_threshold(counts, centers)

    #print 'Sleep : ', ltsleep, '-', htsleep

    # computing threshold for bathroom activity
    [counts, centers] = np.histogram(bath_list)

    counts = counts*(1.0/total_days)

    htbath = cal_high_threshold(counts, centers)
    ltbath = cal_low_threshold(counts, centers)

    #print 'Bath : ', ltbath, '-', htbath


def give_recommendation(pushui, curdate, lang='en'):

    curactive = getActiveness(curdate)

    curroom = getOccupationLevel(curdate)

    curkitchen = 0
    curdinning = 0
    curbath = 0
    curbed = 0
    if curroom != 0:
        if 'HS_Kitchen' in curroom:
            curkitchen = float(curroom['HS_Kitchen'])

        if 'HS_Dining_Room' in curroom:
            curdinning = float(curroom['HS_Dining_Room'])

        if 'HS_Bathroom' in curroom:
            curbath = float(curroom['HS_Bathroom'])

        if 'HS_Bedroom' in curroom:
            curbed = float(curroom['HS_Bedroom'])

    cureat = curdinning + curkitchen

    if cureat < lteat:
        (title, msg) = get_message('lowappetite', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(8),
                            endTime=time(9,30),
                            topic='Activity')

    if cureat > hteat:
        (title, msg) = get_message('highappetite', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(8),
                            endTime=time(9,30),
                            topic='Activity')

    if curbath > htbath:
        (title, msg) = get_message('highbathroom', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(8),
                            endTime=time(10),
                            topic='Activity')

    if curbed < ltsleep:
        (title, msg) = get_message('lowbedroom', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(21),
                            endTime=time(23),
                            topic='Activity')
    if curbed > htsleep:
        (title, msg) = get_message('highbedroom', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(21),
                            endTime=time(23),
                            topic='Activity')

    if curactive < ltactivity:
        (title, msg) = get_message('lowactivity', lang)
        pushui.post_message(title.encode('utf-8'),
                            msg.encode('utf-8'),
                            date=date.today(),
                            startTime=time(12),
                            endTime=time(15),
                            topic='Activity')


class IPIRecommendations(object):
    """ IPIRecommendations class
        The SonopaPushUI should instantiate this class and keep the handle.
        Each night, it should call the 'run_one' function, to generate recommendations
    """

    def __init__(self, settings=None):
        """ Constructor for recommendations class

        :param settings: the settings with which to generate recommendations.
                         should be fully filled in. See below for format.
        :type settings: dict

        """
        if not settings:
            settings = {'language': 'en',
                        'userId': '0',
                        'pushUI': {
                            'uri': 'http://sonopa.c.smartsigns.nl/venuemaster-web-unified/sms/api',
                            'username': '',
                            'password': ''
                            }
                        }
        self.settings = settings
        self.pushui = PushUI(self.settings['pushUI']['uri'],
                             self.settings['pushUI']['username'],
                             self.settings['pushUI']['password'])
        self.pushui.user_id = self.settings['userId']

    def run_once(self, day=None):
        """ Generate recommendations for the given day, and post them to the sonopa
        Push UI.
        This function should be run each night, somewhere after 00:00h, so that
        recommendations will show up on the monitor throughout the day.

        :param day: A datetime object specifying the day to generate
                    recommendations for. If not given, yesterday is picked.
        :type day: datetime or None
        """

        if not day:
            day = datetime.now() - timedelta(days=1)

        get_thresholds(day)
        give_recommendation(self.pushui, day, self.settings['language'])



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Give recommendations',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     conflict_handler='resolve')

    yesterday = datetime.now()
    datestr = yesterday.strftime('%Y%m%d')

    parser.add_argument('-d', '--date', type=str, default=datestr, help='the date to analyse')
    parser.add_argument('-l', '--language', default='en', help='language of the messages (\'nl\', \'en\' or \'fr\')')
    parser.add_argument('-u', '--user-id', default='0', help='id of the user to send messages to')
    parser.add_argument('-p', '--push-ui', type=str, default='http://sonopa.c.smartsigns.nl/venuemaster-web-unified/sms/api', help='uri of the push ui')
    args = parser.parse_args()

    day = datetime.strptime(args.date, "%Y%m%d").date() - timedelta(days=1)

    settings = {'language': args.language,
                'userId': args.user_id,
                'pushUI': {
                    'uri': args.push_ui,
                    'username': '',
                    'password': ''
                    }
                }

    recom = IPIRecommendations(settings)
    recom.run_once(day)
