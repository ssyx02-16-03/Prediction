from AbstractLoader import AbstractLoader
import parse_date


class AverageTimeWaitedLoader(AbstractLoader):
    def set_search_triage(self):
        self.event_name = "TimeToTriage"

    def set_search_doctor(self):
        self.event_name = "TimeToDoctor"

    def set_search_removed(self):
        self.event_name = "TotalTime"

    def load_value(self, time_point, interval_unused):
        """
        This finds every patient in queue at a given time and then calculates how long they have been waiting, on
        average. Like its Loader siblings UntriagedLoader and TimeToEventLoader it will not work unless
        set_search_something is called.

        Plotting this over time yields an interesting saw-toothy graph.

        :param time_point: point in time to analyse
        :param interval_unused: this really is unused, we are looking at a point in time
        :return: average time spent in queue for patients in queue at the given point in time
        """

        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(time_point)

        hits = response["hits"]["hits"]  # dig up list of patients from response
        time_waited = 0
        count = 0
        for patient in hits:
            try:
                time_to_event = patient["fields"][self.event_name][0]
            except KeyError:
                # if no value is found, set time to -1. this is specifically for ongoing patients missing TotalTime
                time_to_event = -1

            care_contact_registration_time = parse_date.date_to_millis(patient["fields"]["CareContactRegistrationTime"][0])
            event_time = care_contact_registration_time + time_to_event

            # if patient was never triaged or if triage had not happened yet
            if time_point < event_time or (time_to_event == -1 and patient["_index"] == "on_going_patient_index"):
                count += 1
                time_waited += (time_point - care_contact_registration_time)

        if count is not 0:
            return time_waited / count
        return -1

    def patients_present(self, time_point):
        """
        :param time_point:
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
                                    "lte": time_point,
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
                                            "gte": time_point,
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


