__author__ = 'hasier'

from app.models import Event, Activity, ActivityModel
from utils import get_timestamp
from datetime import datetime


class Reasoner:
    """Class that consumes sensor events and provides inferred activities"""

    def __init__(self):
        self._events = []
        self._debug = True

    def feed(self, event):
        """Inserts a new sensor event into the reasoner"""
        self._events.append(event)

    def infer_activity(self):
        """Infers whether the previously given sensor events conform a new activity"""
        from random import random
        from math import ceil
        if self._debug:
            r = ceil(random() * 7.0)
            if r < 1.0 or r > 5.0:
                return None
            self._events = []
            am = ActivityModel.query.get(r)
            return Activity(is_a=am, timestamp=datetime.fromtimestamp(get_timestamp()/1000.0))
        else:
            # TODO With the data in self._events check if an activity can be inferred
            return None