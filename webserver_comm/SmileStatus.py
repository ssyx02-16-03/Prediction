from PatientsFlows.QueueTimeGraphs import QueueTimeGraphs
from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
import time

from elastic_api.TimeToEventLoader import TimeToEventLoader

ONE_HOUR_MILLISECONDS = 60*60*1000

# TODO put proper values here, these were improvised
time_to_doctor_hysteresis = 0
time_to_klar_hysteresis = 0
lookback_time = ONE_HOUR_MILLISECONDS / 2  # the ttx value is retreived for the [now - lookback_time] time point to
# decide what the change rate is

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

        loader = TimeToEventConditionalLoader(now - ONE_HOUR_MILLISECONDS * 24, now, 0)

        loader.set_teams(["NAKME"])

        loader.set_torg("medicineBlue")
        loader.set_search_doctor()
        self.ttl_blue_x, self.ttl_blue_y = QueueTimeGraphs(loader).moving_average()

        loader.set_event_name("TimeToFinished")
        self.ttk_blue_x, self.ttk_blue_y = QueueTimeGraphs(loader).moving_average()

        loader.set_torg("medicineYellow")
        loader.set_event_name("TimeToFinished")
        self.ttl_yellow_x, self.ttl_yellow_y = QueueTimeGraphs(loader).moving_average()

        loader.set_search_removed()
        self.ttk_yellow_x, self.ttk_yellow_y = QueueTimeGraphs(loader).moving_average()

    def get_smile_data(self):
        blue = {
            "ttd": {
                "value": int(self.ttl_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttl_blue_x, self.ttl_blue_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttl_blue_y, time_to_doctor_boundaries)
            },
            "ttk": {
                "value": int(self.ttk_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttk_blue_x, self.ttk_blue_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttk_blue_y, time_to_klar_boundaries)
            }
        }
        yellow = {
            "ttd": {
                "value": int(self.ttl_yellow_y[-1]),
                "trend": self._make_smile_arrow(self.ttl_yellow_x, self.ttl_yellow_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttl_yellow_y, time_to_doctor_boundaries)
            },
            "ttk": {
                "value": int(self.ttk_blue_y[-1]),
                "trend": self._make_smile_arrow(self.ttk_yellow_x, self.ttk_yellow_y, time_to_klar_hysteresis),
                "mood": self._make_smile_happiness(self.ttk_yellow_y, time_to_klar_boundaries)
            }
        }

        return blue, yellow

    def _make_smile_arrow(self, x, y, hysteresis):
        v = self._get_velocity(x, y)
        if v > hysteresis:
            return 1
        elif v < -hysteresis:
            return -1
        return 0

    def _get_velocity(self, x, y):
        """
        :param x: vector of timestamps
        :param y: vector of ttx values
        :return: velocity in milliseconds / millisecond
        """
        now = int(time.time()) * 1000
        lookback_point = now - lookback_time
        i = len(x) - 1
        while i > 0 and x[i] > lookback_point:  # find the element in x close to lookback_point
            i -= 1

        # calculate the average velocity between lookback_point and now
        return (y[-1] - y[i]) / lookback_time

    def _make_smile_happiness(self, y, bounds):
        value = y[-1]
        if value < bounds["bad"]:
            return -1
        elif value > bounds["good"]:
            return 1
        return 0

