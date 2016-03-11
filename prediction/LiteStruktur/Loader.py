from abc import ABCMeta, abstractmethod
from elasticsearch import Elasticsearch
import time

class Loader(object):
    # AbstractBaseClass-grej
    __metaclass__ = ABCMeta

    def __init__(self, startTime, endTime, interval):
        self.startTime = self.to_epoch_millis(startTime)
        self.endTime = self.to_epoch_millis(endTime)
        self.interval = interval * 1000 * 60

        with open("../elasticIP.txt") as f:
            elastic = f.readline()
        self.client = Elasticsearch(elastic)

    @abstractmethod
    def load(self):
        """python-kommentar woooo"""
        return

    def set_offset(self, minutes):
        self.startTime = self.startTime + minutes * 1000 * 60
        self.endTime = self.endTime + minutes * 1000 * 60


    def discrete_time(self, continous_time):
        return self.interval * (int((continous_time - 1) / self.interval) + 1)

    def to_epoch_millis(self, date_time):
        epoch = int(time.mktime(time.strptime(date_time, "%Y-%m-%d %H:%M"))) * 1000
        return epoch
