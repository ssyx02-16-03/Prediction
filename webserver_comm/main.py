import time
import AMQCommunication
import RoomOccupation
import BarGraphs
import RoomOverview

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

    room_data = RoomOccupation.run()
    amq.send_package("room_occupation", room_data[0])
    amq.send_package("coordinator_free_rooms", room_data[1])

    amq.send_package("bar_graphs", BarGraphs.run())

    room_overview = RoomOverview.run()
    amq.send_package("blue_side_overview", room_overview["blue"])
    amq.send_package("yellow_side_overview", room_overview["yellow"])

if __name__ == '__main__':
    main()



