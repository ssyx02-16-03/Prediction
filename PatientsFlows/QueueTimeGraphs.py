import numpy as np
import matplotlib.pyplot as plt

from elastic_api import parse_date
from elastic_api.TimeToEventLoader import TimeToEventLoader

ONE_MINUTE_MILLIS = 60000


class QueueTimeGraphs:
    def __init__(self, loader):
        self.loader = loader

        times = loader.get_event_times()  # retrieve all events on the interval
        times = self._filter_zeroes(times)      # only analyse non-zero queue times
        # reformat to numpy column matrix and sort by timestamp
        both_times = np.column_stack(times)

        self.num_events = len(times[0])
        self.event_time_matrix = both_times[np.argsort(both_times[:, 1])]
        self.wait_times = (self.event_time_matrix[:, 1] - self.event_time_matrix[:, 0]) / ONE_MINUTE_MILLIS

        self.event_times = (self.event_time_matrix[:, 1] - self.loader.start_time) / ONE_MINUTE_MILLIS

        if len(self.wait_times) == 0:
            self.wait_times = [0]
        #TODO handle empty input

    def moving_average(self):
        PERCENT_NEW = 0.1
        PERCENT_OLD = 1 - PERCENT_NEW

        wait_means = []
        wait_mean = self.wait_times[0]
        for wait_time in self.wait_times:  # pycharm is giving a warning here but i think it is just confused
            wait_mean = wait_mean * PERCENT_OLD + wait_time * PERCENT_NEW
            wait_means.append(wait_mean)

        wait_means = np.asarray(wait_means)

        return self.event_times, wait_means

    def rolling_average(self, sweep_length, sweep_interval):
        """
        This rolls along the time axis, calculating average event times.
        :param loader: a TimeToEventLoader with set_search() already set
        :param sweep_length: The length of each sample; if set to one hour, every sample will contain the average of all
         events that happened during the previous hour.
        :param sweep_interval: time between samples
        :return: time vector and vector of values
        """

        start_time = self.loader.start_time
        end_time = self.loader.end_time - sweep_length
        return_y = []
        return_x = []

        for time in range(start_time, end_time, sweep_interval):
            # locate the lowest timestamp that is on our interval
            i = 0
            while i < self.num_events and self.event_time_matrix[i][0] < time:
                i += 1
            start_index = i

            # locate the highest timestamp that is still on our interval
            while i < self.num_events and self.event_time_matrix[i][0] < time + sweep_length:
                i += 1
            end_index = i

            # calculate the average time duration of all values between start_index and end_index
            average = 0
            if end_index > start_index:
                for k in range(start_index, end_index):
                    duration = (self.event_time_matrix[k][1] - self.event_time_matrix[k][0]) / ONE_MINUTE_MILLIS
                    average += duration
                average /= (end_index - start_index)
            return_y.append(average)
            return_x.append((time-start_time) / ONE_MINUTE_MILLIS)

        return return_x, return_y

    def matplot_draw(self):
        """
        runs each method in this class and draws results in a matlplot, for testing purposes
        """
        x_moving, y_moving = self.moving_average()
        x_rolling, y_rolling = self.rolling_average(sweep_interval=ONE_MINUTE_MILLIS, sweep_length=ONE_MINUTE_MILLIS*60)

        plt.plot(self.event_times, y_moving, c='blue', label='10% nya')
        plt.plot(x_rolling, y_rolling, c='black', label='Rolling average 60 min')
        plt.scatter(self.event_times, self.wait_times, c='black', marker='x', label='Faktiska TTT-tider')

        plt.legend(loc='upper right')
        plt.show()

    @staticmethod
    def _filter_zeroes(times):
        """
        given a two column matrix, it filters out all lines in the matrix where both values are the same
        used here to filter out all zero-length durations
        """
        filtered_times = [[], []]
        for i in range(0, len(times[0])):
            if times[0][i] != times[1][i]:
                filtered_times[0].append(times[0][i])
                filtered_times[1].append(times[1][i])
        return filtered_times

def test():
    # initialize the loader
    start_time = "2016-03-30 08:00"
    end_time = "2016-03-31 08:00"
    interval = 60
    ttt = TimeToEventLoader(start_time, end_time, interval)
    ttt.set_search_triage()
    QueueTimeGraphs(ttt).matplot_draw()
