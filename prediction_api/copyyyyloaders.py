# -*- coding: utf-8 -*-
""" Module for loading "state"-like paramaters from Elasticsearch.

Methods in this module must take only one argument, timee, a time-variable in
epoch-millis, and return a number. If the returned number represents time, it
should also be in epoch-millis. Other kinds of methods do not belong here.
Private methods that take or return something else should me marked with _.
"""
from ESClient import ESClient
import utils
from threaded_query import threaded_query
import elastic_api.parse_date as pd


def _patients_in_window(time1, time2):

    client = ESClient()
    response = client.search(
        index="*",
        body=
        {
            "size": 10000,
            "query": {
                "match_all": {}
            },
            "filter": {
                "and": [
                    {
                        "range": {
                            "CareContactRegistrationTime": {
                                "lte": time2,
                                "format": "epoch_millis"
                            }
                        }
                    },
                    {
                        "or": [
                            {
                                "match": {
                                    "_index": "on_going_patient_index"
                                }
                            },
                            {
                                "range": {
                                    "RemovedTime": {
                                        "gte": time1,
                                        "format": "epoch_millis"
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }
    )
    return response


def _events_in_window(time1, time2):
    patients_in_window = _patients_in_window(time1, time2)["hits"]["hits"]
    events = []
    for patient in patients_in_window:
        for event in patient["_source"]["Events"]:
            event_time = utils.crapformat1_to_emills(event["Start"])
            if time1 < event_time < time2:
                events.append(event)
    return events


def _current_patients(timee):
    return _patients_in_window(timee, timee)


def ongoings(timee):
    """Return total number of patients present at timee."""
    return _current_patients(timee)["hits"]["total"]


def _waiters(timee, event_name):
    #timee = timee + 2 * 60 * 60 * 1000
    patients = _current_patients(timee)["hits"]["hits"]
    count = 0
    for patient in patients:
        try:
            # TODO bloody sneaky factor of 10, what is up?
            time_to_event = patient["_source"][event_name]
        except KeyError:
            time_to_event = -1
        reg_time_crap = patient["_source"]["CareContactRegistrationTime"]
        #print reg_time_crap
        reg_time = pd.date_to_millis(reg_time_crap)
        #print reg_time
        event_time = reg_time + time_to_event
        in_ong_index = (patient["_index"] == "on_going_patient_index")
        print "timee:         ", timee
        print "event_time:    ", event_time
        print "reg_time:      ", reg_time
        print "time_to_event: ", time_to_event
        print "diff: ", (timee - event_time) / (1000 * 60)
        if timee < event_time:# or time_to_event == -1:
            print "hej"
            count += 1
    return count


def untriageds(timee):
    """Return number of present but untriaged patients."""
    return _waiters(timee, "TimeToTriage")


def doctors(timee):
    """Return number of doctor tags in past hour events."""
    one_hr_bk = timee - 60 * 60 * 1000
    events_in_window = _events_in_window(one_hr_bk, timee)
    doctor_tags = []
    for event in events_in_window:
        if event["Type"] == u"LÄKARE":
            doctor_tags.append(event["Value"])
    unique_doctor_tags = set(doctor_tags)
    return len(unique_doctor_tags)

# test
time1_crap = "2016-03-11 18:30"
time2_crap = "2016-03-11 19:00"
time1 = utils.crapformat2_to_emills(time1_crap)
time2 = utils.crapformat2_to_emills(time2_crap)

time_now_crap = "2016-04-12 19:54"
time_now = pd.date_to_millis(time_now_crap)
print time_now

times = [time_now] * 2
values = threaded_query(untriageds, times)
print values
