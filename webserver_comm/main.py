import time
from AMQCommunicationStomp import AMQCommunicationStomp
import RoomOccupation
import BarGraphs
import RoomOverview
from webserver_comm import RecentChanges
import smile_status
from webserver_comm.QueueStatus import QueueStatus

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

        room_data = RoomOccupation.run()
        self.amq.send_package("room_occupation", room_data[0])
        self.amq.send_package("coordinator_free_rooms", room_data[1])

        bars = BarGraphs.run()
        self.amq.send_package("bar_graphs", bars)

        room_overview = RoomOverview.run()
        self.amq.send_package("blue_side_overview", room_overview["blue"])
        self.amq.send_package("yellow_side_overview", room_overview["yellow"])

        updates = RecentChanges.run()
        self.amq.send_package("recent_changes", updates)

        queue_status = QueueStatus()

        graph = queue_status.get_line_graph_data()
        self.amq.send_package("coordinator_line_graph", graph)

        smiles_blue, smile_yellow = queue_status.get_smile_data()
        self.amq.send_package("smile_face_blue", smiles_blue)
        self.amq.send_package("smile_face_yellow", smile_yellow)


def run():
    print "starting..."
    Main().main()
