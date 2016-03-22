# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import os
import time
import numpy as np

class PresentTTT(object):

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
        ttt = np.array([])

        for patient in patients:
            patient_ttt = patient['_source']['TimeToTriage']

            if patient_ttt > 0:
                bad_format_seat_time = patient['_source']['CareContactRegistrationTime']
                patient_seat_time = int(time.mktime(time.strptime(bad_format_seat_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000

                seat_times = np.append(seat_times, patient_seat_time)
                ttt = np.append(ttt, patient_ttt)

        self.ttt = ttt
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

    def get_ttt(self):
        """
        :return: vektor med TTT
        """
        return self.ttt

    def get_seat_time(self):
        """
        :return: vektor med tider då patienterna började vänta på triage
        """
        return self.seat_time


