# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import os
import time
import numpy as np

from datetime import datetime

class TTD(object):

    def __init__(self, time1, time2):
        """
        :param time1: format: "2016-03-06 23:18"
        :param time2:
        """
        time1_millis = int(time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M"))) * 1000
        time2_millis = int(time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M"))) * 1000

        response = self.get_patients(time1_millis, time2_millis)

        patients = response['hits']['hits']

        seat_times = np.array([])
        ttd = np.array([])

        for patient in patients:
            patient_ttd = int(patient['_source']['TimeToDoctor'])

            if patient_ttd > 0:
                bad_format_seat_time = patient['_source']['CareContactRegistrationTime']
                patient_seat_time = int(time.mktime(time.strptime(bad_format_seat_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000

                seat_times = np.append(seat_times, int(patient_seat_time))
                ttd = np.append(ttd, patient_ttd)

        self.ttd = ttd
        self.seat_time = seat_times


    def get_patients(self, time1_millis, time2_millis):
        file_name = os.path.join(os.path.dirname(__file__), '../elasticIP.txt')
        with open(file_name) as f:
            elastic = f.readline()

        client = Elasticsearch(elastic)

        return client.search(
            index = "*",
            body =
            {
                "size": 1000,
                "query": {
                    "match_all": { }
                },
                "filter": {
                    "range": {
                        "CareContactRegistrationTime": {
                            "gte": time1_millis,
                            "lte": time2_millis,
                            "format": "epoch_millis"
                        }
                    }
                }
            }
        )

    def get_ttd(self):
        """
        :return: vektor med TTD
        """
        return self.ttd

    def get_seat_time(self):
        """
        :return: vektor med tider då patienterna började vänta på triage
        """
        return self.seat_time

    def get_weekday(self, timee):
        day_string = datetime.fromtimestamp(timee/1000).strftime("%A")
        day_int_map = {
                'Monday': 1,
                'Tuesday': 2,
                'Wednesday': 3,
                'Thursday': 4,
                'Friday': 5,
                'Saturday': 6,
                'Sunday': 7
            }
        return int(day_int_map[day_string])

    def get_weekdays(self):
        """
        :return: vektor med 1 för måndag, 2 för tisdag osv
        """
        weekdays = np.array([])
        for timee in self.seat_time:
            weekdays = np.append(weekdays, self.get_weekday(timee))
        return weekdays

    def get_daytime(self, timee):
        # resten vid division med millisar på en dag borde la bli rätt
        return int((timee % (1000 * 60 * 60 * 24)) / 1000)

    def get_daytimes(self):
        """
        :return: vektor med tid på dagen i sekunder
        """
        daytimes = np.array([])
        for timee in self.seat_time:
            daytimes = np.append(daytimes, self.get_daytime(timee))
        return daytimes

    def get_weektimes(self):
        """
        :return: vektor med timmen i veckan (>0, <180ish)
        """
        return self.get_weekdays() * 24 + self.get_daytimes() / 3600
