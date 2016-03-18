from elastic_api.TimeToEventLoader import TimeToEventLoader
import time


class TimeToEvent:
    @staticmethod
    def run(title, points, interval):
        """
        Calculates historic values for TTT, TTD or TTK. For each interval, calcuates the TTX for the patients that
        underwent event X during that interval.
        :param title: the event title to look for. Must be one of ["Triage", "Doctor, "Removed"]
        :param points: number of sample points
        :param interval: the time between sample points
        :return: a list containing the average time_to_event for each sample point
        """
        loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)  # constructor parameters are unused

        if title is "Triage":
            loader.set_search_triage()
        elif title is "Doctor":
            loader.set_search_doctor()
        elif title is "Removed":
            loader.set_search_removed()
        else:
            raise NameError

        times = []
        for n in range(1, points):
            times.append(loader.load_value(int(time.time() * 1000) - interval * n, interval))
        return times

