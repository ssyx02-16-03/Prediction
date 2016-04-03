import time
import AMQCommunication
from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
import json

import RoomOccupation
import TimeToEvent
import CoordinatorBarGraph

FRAME_TIME_INTERVAL = 0.5  # seconds
amq = AMQCommunication.AMQCommunication()
ONE_HOUR_MILLISECS = 60*60*1000


def main():
    """
    Calls iteration() with FRAME_TIME_INTERVAL intervals
    """
    while 1:
        last_time = time.time()
        iteration()
        if last_time + FRAME_TIME_INTERVAL - time.time() > 0:
            time.sleep(last_time + FRAME_TIME_INTERVAL - time.time())


def iteration():
    """
    One run of the loop.
    """

    data = RoomOccupation.run()[0]
    amq.send_package("room_occupation", data)

    data = RoomOccupation.run()[1]
    amq.send_package("coordinator_free_rooms", data)

    data = CoordinatorBarGraph.run()
    amq.send_package("bar_graphs", data)

if __name__ == '__main__':
    main()

s


