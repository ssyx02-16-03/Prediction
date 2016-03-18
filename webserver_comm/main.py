import time
import AMQCommunication
from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
import json

from RoomOccupation import RoomOccupation
from TimeToEvent import TimeToEvent

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
    data = TimeToEvent.run("Triage", 10, ONE_HOUR_MILLISECS)
    amq.send_package("triage_times_array", data)

    data = TimeToEvent.run("Doctor", 10, ONE_HOUR_MILLISECS)
    amq.send_package("doctor_times_array", data)

    data = TimeToEvent.run("Removed", 10, ONE_HOUR_MILLISECS)
    amq.send_package("removed_times_array", data)

    data = RoomOccupation.run()
    amq.send_package("room_occupation", data)

if __name__ == '__main__':
    main()




