from PatientsFlows.QueueTimeGraphs import QueueTimeGraphs
from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
import time

ONE_HOUR_MILLISECONDS = 60000

# TODO put proper values here, these were improvised
time_to_doctor_hysteresis = 10
time_to_klar_hysteresis = 100

time_to_doctor_boundaries = {
    "bad": 20,
    "good": 50
}
time_to_klar_boundaries = {
    "bad": 100,
    "good": 300
}

class SmileStatus:
    def __init__(self):
        now = int(time.time()) * 1000

        loader = TimeToEventConditionalLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
        loader.end_time = now
        loader.start_time = now - ONE_HOUR_MILLISECONDS * 24
        loader.set_teams(["NAKME"])

        loader.set_torg("medicineBlue")
        loader.set_search_doctor()
        self.ttl_blue_x, self.ttl_blue_y = QueueTimeGraphs(loader).moving_average()

        loader.set_search_removed()
        self.ttk_blue_x, self.ttk_blue_y = QueueTimeGraphs(loader).moving_average()

        loader.set_torg("medicineYellow")
        loader.set_search_doctor()
        self.ttl_yellow_x, self.ttl_yellow_y = QueueTimeGraphs(loader).moving_average()

        loader.set_search_removed()
        self.ttk_yellow_x, self.ttk_yellow_y = QueueTimeGraphs(loader).moving_average()

    def get_smile_data(self):
        blue = {
            "ttd": {
                "value": int(self.ttl_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttl_blue_x, self.ttl_blue_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttl_blue_x, self.ttl_blue_y, time_to_doctor_boundaries)
            },
            "ttk": {
                "value": int(self.ttk_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttk_blue_x, self.ttk_blue_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttk_blue_x, self.ttk_blue_y, time_to_klar_boundaries)
            }
        }
        yellow = {
            "ttd": {
                "value": int(self.ttl_yellow_y[-1]),
                "trend": self._make_smile_arrow(self.ttl_yellow_x, self.ttl_yellow_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttl_yellow_x, self.ttl_yellow_y, time_to_doctor_boundaries)
            },
            "ttk": {
                "value": int(self.ttk_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttk_yellow_x, self.ttk_yellow_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttk_yellow_x, self.ttk_yellow_y, time_to_klar_boundaries)
            }
        }

        return blue, yellow

    def _make_smile_arrow(self, x, y, hysteresis):
        # TODO do this thing
        return 1

    def _make_smile_happiness(self, x, y, bounds):
        value = y[-1]
        if value < bounds["bad"]:
            return -1
        elif value > bounds["good"]:
            return 1
        return 0

