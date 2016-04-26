from abc import ABCMeta, abstractmethod
from datetime import datetime

from elasticsearch import Elasticsearch
import numpy as np
import time
import os

class AbstractLoader(object):

    # AbstractBaseClass-grej
    __metaclass__ = ABCMeta

    def __init__(self, start_time, end_time, interval_minutes):
        """
        :param start_time: format: "2016-03-06 23:18" eller epoch_milli int
        :param end_time: format:
        :param interval_minutes: i minuter = en int
        """
        if isinstance(start_time, int) or isinstance(start_time, float):
            self.start_time = start_time
            self.end_time = end_time
        else:
            self.start_time = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M"))) * 1000
            self.end_time = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M"))) * 1000
        self.interval = interval_minutes * 1000 * 60

        file_name = os.path.join(os.path.dirname(__file__), 'elasticIP.txt')
        with open(file_name) as f:
            elastic = f.readline()
        self.client = Elasticsearch(elastic)

    @abstractmethod
    def load_value(self, time, interval):
        """
        :param time: i epoch_millis, sa ange i ES-queryn att det ar det!
        :param interval: interval fram till time, i epoch_millis, maste ej anvandas
        :return: ETT varde for tidpunkten time eller tidsintervallet fram till time
        """

    def load_vector(self):
        """
        :return: kolonnvektor med samma langd som antal features, dvs formatet sklearn vill ha
        """
        vector = [None] * self.iterations()
        for i in range(self.iterations()):
            vector[i] = self.load_value(self.start_time + (i + 1) * self.interval, self.interval)
        return np.asarray(vector)

    def set_offset(self, offset_minutes):
        """
        anvandning ex: om du vill veta en vantetid tva timmar framat i tiden relativt in-paramterarna, satt offset 120
        :param offset_minutes: i minuter = en int
        """
        self.start_time = self.start_time + offset_minutes * 1000 * 60
        self.end_time = self.end_time + offset_minutes * 1000 * 60

    def to_epoch_millis(self, date_time):
        """
        konverterar tidsformatet i databasen till epoch_millis
        :param date_time: format: "2016-03-07T03:52:00Z"
        :return: tiden i epoch_millis
        """
        return int(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000

    def iterations(self):
        return int((self.end_time - self.start_time)/self.interval)

    def get_times_of_day(self):
        times = []
        for i in range(0, (self.end_time-self.start_time)/(self.interval), 1):
            times.append((i*self.interval/(60*60*1000))%24)
        return times

    def get_weekdays(self):
        days = []
        for i in range(self.start_time, self.end_time, self.interval):
            days.append(datetime.fromtimestamp(i/1000).weekday())

    def get_times(self):
        """
        :return: vektorn med tider, i epoch_millis
        """
        return np.linspace(self.start_time + self.interval, self.end_time, self.iterations())
