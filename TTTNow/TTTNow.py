from elasticsearch import Elasticsearch
import os
import time
import numpy as np

def get_patients(time1, time2):
    """
    :param time1: format: "2016-03-06 23:18"
    :param time2:
    :return: elastic response
    """
    time1_millis = int(time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M"))) * 1000
    time2_millis = int(time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M"))) * 1000

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

time1 = "2016-03-10 10:00"
time2 = "2016-03-10 11:00"

response = get_patients(time1, time2)

patients = response['hits']['hits']

data = []

for patient in patients:
    ttt = patient['_source']['TimeToTriage']

    if ttt > 0:
        data.append({'TTT': ttt,
                     'CareContactRegistrationTime': patient['_source']['CareContactRegistrationTime']})

print len(data)