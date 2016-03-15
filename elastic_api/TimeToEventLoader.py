from AbstractLoader import AbstractLoader
import time


class TimeToEventLoader(AbstractLoader):
    def set_search_triage(self):
        self.event_name = "TimeToTriage"

    def set_search_doctor(self):
        self.event_name = "TimeToDoctor"

    def set_search_removed(self):
        self.event_name = "TotalTime"

    def load_value(self, start_time, interval_minutes):
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

        end_time = start_time + interval_minutes * 60 * 1000

        # i'm afraid i have to do this
        end_time_timezone_fulhack = start_time + (interval_minutes+60) * 60 * 1000  # TODO remove when timezones are fixed

        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(start_time, end_time_timezone_fulhack)

        event_times = []
        hits = response["hits"]["hits"]  # dig up list of patients from response
        for patient in hits:
            try:
                time_to_event = patient["fields"][self.event_name][0]
            except KeyError:
                # if no value is found, set time to -1. this is specifically for ongoing patients missing TotalTime
                time_to_event = -1

            care_contact_registration_time = date_to_millis(patient["fields"]["CareContactRegistrationTime"][0])
            event_time = care_contact_registration_time + time_to_event

            # if triage happened on our interval, add time_to_triage to the list of times
            if time_to_event != -1 and start_time < event_time < end_time:
                event_times.insert(0, time_to_event)

        return event_times

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


def date_to_millis(date):
    """
    transform a non-timezoned date to epoch-millis. If date is timezoned it will crash.
    """
    return long(time.mktime(time.strptime(date, u"%Y-%m-%dT%H:%M:%SZ"))) * 1000

