# -*- coding: utf-8 -*-
# denna kommentar måste va med för åäö

from AbstractLoader import AbstractLoader

# baseklass till alla klasser nedan
class WaitTimeLoader(AbstractLoader):

    event_title = ""

    def load_value(self, time, interval):

        ten_hours_back = time - interval - 10 * 60 * 60 * 1000 # overdrivet?
        four_hours_ahead = time + interval + 4 * 60 * 60 * 1000

        response = self.client.search(
            index = "*",
            body =
            {
                "size": 10000,
                "query": {
                    "match_all": { }
                },
                "filter": {
                    "range": {
                        "CareContactRegistrationTime": {
                            "gte": ten_hours_back,
                            "lte": four_hours_ahead,
                            "format": "epoch_millis"
                        }
                    }
                }
            }
        )

        return self.average_wait_time(response["hits"]["hits"], time, interval)

    def average_wait_time(self, hits, time, interval):

        wait_time = 0;
        count = 0;

        for hit in hits:
            for event in hit["_source"]["Events"]:
                if event["Title"] == self.event_title:
                    event_time = self.to_epoch_millis(event["End"])
                    if time - interval < event_time and event_time < time:
                        count += 1
                        wait_time += event_time - self.to_epoch_millis(hit["_source"]["CareContactRegistrationTime"])

        if count != 0:
            return wait_time / count
        else:
            return 0

    def set_event(self, event_title):
        """
        :param event_title: ex "Triage"
        """
        self.event_title = event_title

class TTTLoader(WaitTimeLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_event(u"Triage")
        super(TTTLoader, self).__init__(start_time, end_time, interval_minutes)

class TTDLoader(WaitTimeLoader):

    def __init__(self, start_time, end_time, interval_minutes):
        self.set_event(u"Läkare")
        super(TTDLoader, self).__init__(start_time, end_time, interval_minutes)

