from AbstractLoader import AbstractLoader
import time
import parse_date


class TimeToEventLoader(AbstractLoader):
    def set_search_triage(self):
        self.event_name = "TimeToTriage"

    def set_search_doctor(self):
        self.event_name = "TimeToDoctor"

    def set_search_removed(self):
        self.event_name = "TotalTime"

    def set_event_name(self, name):
        """
        more convenient way of setting the event type to search for
        """
        self.event_name = name

    def load_value(self, start_time, interval_millisecs):
        """
        Returns a list of values for TTT, TTD or TTK from a given interval. One time value is added to the list for each
        patient that was triaged/doctored/finished during the interval. This method will not cooperate unless one of the
        set_search methods are called first.

        :param start_time: start time for the search in epoch-millis
        :param interval_minutes: duration of the search; is added to time_point to calculate end_time
        :return: list of time_to_event in milliseconds
        """

        if self.event_name is None:  # if set_search_x has not been called, initiate self destruct
            raise Exception  # it actually crashes before it can throw the exception but this looks nice

        end_time = start_time + interval_millisecs

        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(start_time, end_time)

        event_times = []
        hits = response["hits"]["hits"]  # dig up list of patients from response
        for patient in hits:
            try:
                time_to_event = patient["fields"][self.event_name][0]
            except KeyError:
                # if no value is found, set time to -1. this is specifically for ongoing patients missing TotalTime
                time_to_event = -1

            care_contact_registration_time = parse_date.date_to_millis(patient["fields"]["CareContactRegistrationTime"][0])
            event_time = care_contact_registration_time + time_to_event

            # if triage happened on our interval, add time_to_triage to the list of times
            if time_to_event != -1 and start_time <= event_time < end_time:
                event_times.append(time_to_event)

        # calculate average time from list of times and return
        # print event_times
        t = 0
        n = 0
        for event_time in event_times:
            t += event_time
            n += 1

        if n is not 0:  # check for division by zero
            return t / n
        else:
            return -1  # if list is empty, return -1

    def get_event_times(self):
        start_time = self.start_time
        end_time = self.end_time

        if self.event_name is None:  # if set_search_x has not been called, initiate self destruct
            raise Exception  # it actually crashes before it can throw the exception but this looks nice

        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(start_time, end_time)

        event_times = []
        arrivial_times = []
        to_event_times = []

        hits = response["hits"]["hits"]  # dig up list of patients from response
        for patient in hits:
            try:
                time_to_event = patient["fields"][self.event_name][0]
            except KeyError:
                # if no value is found, set time to -1. this is specifically for ongoing patients missing TotalTime
                time_to_event = -1

            care_contact_registration_time = parse_date.date_to_millis(patient["fields"]["CareContactRegistrationTime"][0])
            event_time = care_contact_registration_time + time_to_event

            # if triage happened on our interval, add time_to_triage to the list of times
            if time_to_event != -1 and start_time <= event_time < end_time:
                event_times.append(event_time)
                arrivial_times.append(care_contact_registration_time)
                to_event_times.append(time_to_event)
        return arrivial_times, event_times, to_event_times


    def patients_present(self, start_time, end_time):
        """
        :return: query of all patients that were present at any point in time between start_time and end_time, including
        those who came and/or left during the interval)
        """
        return self.client.search(
            index="*",
            body=
            {
                "size": 10000,
                "fields": ["CareContactRegistrationTime", self.event_name],
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "and": [
                        {
                            "range": {
                                "CareContactRegistrationTime": {
                                    "lte": end_time,
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
                                            "gte": start_time,
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


