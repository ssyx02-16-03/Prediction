import time
import AMQCommunication
import RoomOccupation
import BarGraphs
import RoomOverview
import coordinator_line_graphs
from webserver_comm import RecentChanges
import smile_status

FRAME_TIME_INTERVAL = 0.5  # seconds
ONE_HOUR_MILLISECS = 60*60*1000


class Main:
    def main(self):
        """
        Calls iteration() with FRAME_TIME_INTERVAL intervals
        """
        self.amq = AMQCommunication.AMQCommunication()
        while 1:
            last_time = time.time()
            self.iteration()
            if last_time + FRAME_TIME_INTERVAL - time.time() > 0:
                time.sleep(last_time + FRAME_TIME_INTERVAL - time.time())

    def iteration(self):
        """
        One run of the loop.
        """

        room_data = RoomOccupation.run()
        self.amq.send_package("room_occupation", room_data[0])
        self.amq.send_package("coordinator_free_rooms", room_data[1])

        self.amq.send_package("bar_graphs", BarGraphs.run())

        room_overview = RoomOverview.run()
        self.amq.send_package("blue_side_overview", room_overview["blue"])
        self.amq.send_package("yellow_side_overview", room_overview["yellow"])

        updates = RecentChanges.run()
        self.amq.send_package("recent_changes", updates)

        graph = coordinator_line_graphs.run()
        self.amq.send_package("coordinator_line_graph", graph)

        #smile_status.run()



def run():
    print "starting..."
    Main().main()


if __name__ == '__main__':
    run()
