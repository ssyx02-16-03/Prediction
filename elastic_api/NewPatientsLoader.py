from AbstractLoader import AbstractLoader
import numpy as np
import time

class NewPatientsLoader(AbstractLoader):

    def load_value(self, **kwargs):
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
                            "gte": self.start_time,
                            "lte": self.end_time,
                            "format": "epoch_millis"
                        }
                    }
                }
            }
        )

        return self.bundle(response['hits']['hits'])


    def bundle(self, response):
        ttt = [0] * int((self.end_time - self.start_time)/self.interval)

        for hit in response:
            continousTime = self.kass_converter(hit["_source"]["VisitRegistrationTime"])
            discreteTime = self.discrete_time(continousTime)
            ttt[(discreteTime - self.start_time)/self.interval] = ttt[(discreteTime - self.start_time)/self.interval] + 1

        return np.asarray(ttt)

    def kass_converter(self, date_time):
        epoch = int(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ"))) * 1000
        return epoch

    def discrete_time(self, continous_time):
        return self.interval * (int((continous_time - 1) / self.interval) + 1)