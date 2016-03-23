from AbstractLoader import AbstractLoader
import parse_date


class AverageTimeWaitedLoader(AbstractLoader):
    def load_value(self, time_point, interval_unused):
        # Get all patients that were present at any time during hte given interval
        response = self.patients_present(time_point)

        hits = response["hits"]["hits"]  # dig up list of patients from response
        time_waited = 0
        count = 0
        for patient in hits:
            time_to_event = patient["fields"]["TimeToTriage"][0]
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


