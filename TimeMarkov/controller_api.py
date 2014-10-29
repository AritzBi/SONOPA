__author__ = 'hasier'

import HybridTimeMarkovNX
from os.path import isfile
from models import Anomaly


class ControllerAPI:

    def __init__(self, backup_path=None):
        """
        Create a new ControllerAPI object to connect to the activity model.

        If backup_path is given and that file exists, it will be used to restore a previously stored model.
        """
        self._chain = HybridTimeMarkovNX.Markov()
        if not backup_path is None and isfile(backup_path):
            print 'Loading model backup from ' + backup_path
            with open(backup_path, 'r') as f:
                self._chain.import_json(f.read())
        self._last_time = None

    def new_sensor_event(self, activity, time):
        """
        Appends a new event that happened at a given time to the activity model.
        """
        if not self._last_time is None:
            time_diff = time - self._last_time
            self._chain.new_event(time_diff, activity)
        else:
            self._chain.init_lasts(activity, time)
        self._last_time = time

    def check_anomaly(self, activity_name):
        """
        Checks if there is any anomaly in the underlying activity model.
        """
        # TODO Check if an anomaly has been detected in the model
        return None

    def get_serialized_model(self):
        """
        Serializes and returns the underlying activity model.
        """
        return self._chain.export_json()

    def exit_training(self):
        """
        Terminates the training period of the underlying activity model
        """
        self._chain.set_training(False)

    def backup(self, path):
        """
        Backups to the specified path the current status of the underlying activity model
        """
        j = self._chain.export_json()
        with open(path, 'w+') as f:
            f.write(j)