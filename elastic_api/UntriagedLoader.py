from AbstractLoader import AbstractLoader
import parse_date


class UntriagedLoader(AbstractLoader):
    """
    This class can also count how many patients are waiting for doctor
    """

    def set_search_triage(self):
        self.event_name = "TimeToTriage"

    def set_search_doctor(self):
        self.event_name = "TimeToDoctor"

    def load_value(self, time_point, interval_unused):
        """
        This simply counts how many patients were waiting for triage or doctor at a given time.
        set_search_triage or set_search_doctor must be called before calling this method.

        :param time_point: point in time of sample
        :param interval_unused: this really does nothing, is here to keep the abstract super method happy.
        :return:
        """

        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(time_point)

        hits = response["hits"]["hits"]  # dig up list of patients from response
        count = 0
        for patient in hits:
            time_to_event = patient["fields"]["TimeToTriage"][0]
            care_contact_registration_time = parse_date.date_to_millis(patient["fields"]["CareContactRegistrationTime"][0])
            event_time = care_contact_registration_time + time_to_event

            # if patient was never triaged or if triage had not happened yet
            if time_point < event_time or (time_to_event == -1 and patient["_index"] == "on_going_patient_index"):
                count += 1

        return count

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
                "fields": ["CareContactRegistrationTime", "TimeToTriage"],
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
