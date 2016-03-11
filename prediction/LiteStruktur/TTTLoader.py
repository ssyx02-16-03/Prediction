from Loader import Loader
import numpy as np
import time

class TTTLoader(Loader):

    def load(self):

        ttt = [None] * int((self.endTime - self.startTime)/self.interval)

        for i in np.arange(int((self.endTime - self.startTime)/self.interval)):

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
                                        "gte": self.startTime + (i - 1) * self.interval,
                                        "lte": self.startTime + i * self.interval,
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

            ttt[i] = self.averageTTT(response['hits']['hits'])

        return np.asarray(ttt)

        #return self.bundle(response['hits']['hits'])

    def averageTTT(self, response):
        sum = 0
        iterations = 0
        for hit in response:
            sum = sum + hit["_source"]["TimeToTriage"]
            iterations = iterations + 1
        return sum/iterations

    '''
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
    '''

'''
startTime = "2016-03-06 00:00"
endTime = "2016-03-07 00:00"
interval = 60

ttt = TTTLoader(startTime, endTime, interval)
delayed_ttt = TTTLoader(startTime, endTime, interval)
delayed_ttt.set_offset(120)
x = ttt.load()
delayed_x = delayed_ttt.load()

print x.shape
print x
print delayed_x
'''