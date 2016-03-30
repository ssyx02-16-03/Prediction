from AbstractLoader import AbstractLoader
import parse_date
import time


class PresentButFinishedLoader(AbstractLoader):
    def load_value(self, time_point, interval_unused):
        """
        returns the number of patients that had received the "Klar" event but were still in the sysytem at the given
        time.

        :param start_time: start time for the search in epoch-millis
        :param interval_millisecs: duration of the search; is added to time_point to calculate end_time
        :return: list of time_to_event in milliseconds
        """

        # Get all patients that were present at any time during the given interval
        response = self.patients_present(time_point, time_point)

        hits = response["hits"]["hits"]  # dig up list of patients from response
        n = 0

        for patient in hits:
            events = patient["_source"]["Events"]
            for event in events:
                if event["Title"] == "Klar":
                    klar_time = parse_date.date_to_millis(event["Start"])
                    if klar_time < time_point:
                        n += 1
                        break
        return n

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
                "_source": ["Events"],
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


