from Loader import Loader
import numpy as np
import time

class TTTLoader(Loader):

    def load(self):
        response = self.client.search(
            index="*",
            body =
            {
                "size": 10000,
                "query": {
                "match_all" : { }
                },
                "filter": {
                    "and": [
                        {
                            "range": {
                                "VisitRegistrationTime": {
                                    "gte": self.startTime,
                                    "lte": self.endTime,
                                    "format": "epoch_millis"
                                }
                            }
                        },
                        {
                            "range": {
                                "TimeToTriage": {
                                    "gte": 0
                                }
                            }
                        }
                    ]
                }
            }
        )

        return self.bundle(response['hits']['hits'])

    def bundle(self, response):
        ttt = [None] * int((self.endTime - self.startTime)/self.interval)

        for hit in response:

            continousTime = self.kass_converter(hit["_source"]["VisitRegistrationTime"])
            discreteTime = self.discrete_time(continousTime)
            ttt[(discreteTime - self.startTime)/self.interval] = hit["_source"]["TimeToTriage"]

        return np.asarray(ttt)

    def kass_converter(self, date_time):
        epoch = int(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000
        return epoch

