__author__ = 'hasier'

from time import time


class Anomaly:
    def __init__(self, activity_id, activity_name, anomaly_id, timestamp=time()):
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.id = anomaly_id
        self.timestamp = timestamp