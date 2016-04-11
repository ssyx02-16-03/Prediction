import time
from AMQCommunicationStomp import AMQCommunicationStomp
import RoomOccupation
import BarGraphs
import RoomOverview
import coordinator_line_graphs
from webserver_comm import RecentChanges
import smile_status

FRAME_TIME_INTERVAL = 1  # seconds
ONE_HOUR_MILLISECS = 60*60*1000


class Main:
    def main(self):
        """
        Calls iteration() with FRAME_TIME_INTERVAL intervals
        """
        self.amq = AMQCommunicationStomp()
        while 1:
            last_time = time.time()
            self.iteration()
            if last_time + FRAME_TIME_INTERVAL - time.time() > 0:
                time.sleep(last_time + FRAME_TIME_INTERVAL - time.time())

    def iteration(self):
        """
        One run of the loop.
        """
        try:
            room_data = RoomOccupation.run()
            self.amq.send_package("room_occupation", room_data[0])
            self.amq.send_package("coordinator_free_rooms", room_data[1])
        except Exception:
            pass

        try:
            self.amq.send_package("bar_graphs", BarGraphs.run())
        except Exception:
            pass

        try:
            room_overview = RoomOverview.run()
            self.amq.send_package("blue_side_overview", room_overview["blue"])
            self.amq.send_package("yellow_side_overview", room_overview["yellow"])
        except Exception:
            pass

        try:
            updates = RecentChanges.run()
            self.amq.send_package("recent_changes", updates)

            graph = coordinator_line_graphs.run()
            self.amq.send_package("coordinator_line_graph", graph)
        except Exception:
            pass
        try:

            smile = smile_status.run()
            self.amq.send_package("smile_face_blue", smile["blue"])
            self.amq.send_package("smile_face_yellow", smile["yellow"])
        except Exception:
            pass



def run():
    print "starting..."
    Main().main()


