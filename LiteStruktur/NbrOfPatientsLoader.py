from Loader import Loader
import numpy as np
import time

class NbrOfPatientsLoader(Loader):

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
                    "range": {
                        "VisitRegistrationTime": {
                            "gte": self.startTime,
                            "lte": self.endTime,
                            "format": "epoch_millis"
                        }
                    }
                }
            }
        )

        return self.bundle(response['hits']['hits'])


    def bundle(self, response):
        ttt = [0] * int((self.endTime - self.startTime)/self.interval)

        for hit in response:
            continousTime = self.kass_converter(hit["_source"]["VisitRegistrationTime"])
            discreteTime = self.discrete_time(continousTime)
            ttt[(discreteTime - self.startTime)/self.interval] = ttt[(discreteTime - self.startTime)/self.interval] + 1

        return np.asarray(ttt)

    def kass_converter(self, date_time):
        epoch = int(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000
        return epoch
