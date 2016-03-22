from AbstractLoader import AbstractLoader


class OngoingsLoader(AbstractLoader):

    # for subklasserna
    range = { }
    match = { }

    def load_value(self, time, interval_minutes):

        response = self.client.search(
            index = "*",
            body =
            {
                "size": 0,
                "query": {
                    "match_all": { }
                },
                "filter": {
                    "and": [
                        {
                            "range": {
                                "CareContactRegistrationTime": {
                                    "lte": time,
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
                                            "gte": time,
                                            "format": "epoch_millis"
                                        }
                                    }
                                }
                            ]
                        },
                        self.range,
                        self.match
                    ]
                }
            }
        )

        return response["hits"]["total"]

    def set_range(self, range):
        """
        :param range: range-objekt enligt elastics syntax, ex: {"range": {"RemovedTime": {...}}
        """
        self.range = range

    def set_match(self, match):
        """
        :param match: match-objekt enligt elastics syntax, ex: {"match": {"Priority": "Gul"}}
        """
        self.match = match

