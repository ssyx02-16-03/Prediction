import numpy as np
import matplotlib.pyplot as plt

from elastic_api import parse_date
from elastic_api.TimeToEventLoader import TimeToEventLoader
ONE_MINUTE_MILLIS = 60000


def filter_zeroes(times):
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


def moving_average(loader):
    percent_new = 0.2
    percent_old = 1-percent_new

    times = loader.get_event_times()
    times = filter_zeroes(times) # filter out all zero event times. (patient was never even in the queue)
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:, 1])]

    arr_times = both_times[:, 0]
    event_times = both_times[:, 1]
    wait_times = (both_times[:, 1]-both_times[:, 0])/60000
    arr_times = np.asanyarray(arr_times)[:, np.newaxis]
    event_times = np.asanyarray(event_times)[:, np.newaxis]

    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):
        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)

    X = (event_times-loader.start_time)/60000
    return X, wait_means, wait_times


def exp_moving_average(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def rolling_average(loader, sweep_length, sweep_interval):
    """
    This rolls along the time axis, calculating average event times.
    :param loader: a TimeToEventLoader with set_search() already set
    :param sweep_length: The length of each sample; if set to one hour, every sample will contain the average of all
     events that happened during the previous hour.
    :param sweep_interval: time between samples
    :return: time vector and vector of values
    """
    times = loader.get_event_times()  # retrieve all events on the interval
    times = filter_zeroes(times)      # only analyse non-zero queue times
    # reformat to numpy column thing and sort by timestamp
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:, 1])]

    start_time = loader.start_time
    end_time = loader.end_time - sweep_length
    return_y = []
    return_x = []

    for time in range(start_time, end_time, sweep_interval):
        # locate the lowest timestamp that is on our interval
        i = 0

        length = len(times[0])
        while i < length and both_times[i][0] < time:
            i += 1
        start_index = i

        # locate the highest timestamp that is still on our interval
        while i < length and both_times[i][0] < time + sweep_length:
            i += 1
        end_index = i

        # calculate the average time duration of all values between start_index and end_index
        average = 0
        if end_index > start_index:
            for k in range(start_index, end_index):
                duration = (both_times[k][1] - both_times[k][0]) / ONE_MINUTE_MILLIS
                average += duration
            average /= (end_index - start_index)
        return_y.append(average)
        return_x.append((time-start_time) / ONE_MINUTE_MILLIS)

    return return_x, return_y


# initialize the loader
start_time = "2016-05-03 11:00"
end_time = "2016-05-04 11:00"
interval = 60
start_time_min = parse_date.date_to_millis(start_time) / ONE_MINUTE_MILLIS
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time)) / ONE_MINUTE_MILLIS
ttt = TimeToEventLoader(start_time, end_time, interval)
ttt.set_search_doctor()
X2 = ttt.get_times()[:, np.newaxis]
X2 = (X2/ONE_MINUTE_MILLIS-start_time_min)+interval*2


X1, y1, y2 = moving_average(ttt)
plt.plot(X1, y1, c='blue', label='10% nya')
plt.scatter(X1, y2, c='black', marker='x', label='Faktiska TTT-tider')

y3 = np.convolve(y2, np.ones((10,))/10, mode='same')
plt.plot(X1, y3, c='cyan', label='Glidande 10p')

y4 = np.convolve(y2, np.ones((30,))/30, mode='same')
plt.plot(X1, y4, c='green', label='Glidande 30p')

y5 = ttt.load_vector()/ONE_MINUTE_MILLIS
plt.plot(X2, y5, c='purple', label='60 min medel')

y6 = exp_moving_average(y2, 10)
plt.plot(X1, y6, c='orange', label='Exp glidande 10p')

X_rolling, y_rolling = rolling_average(loader=ttt, sweep_interval=ONE_MINUTE_MILLIS, sweep_length=ONE_MINUTE_MILLIS*60)
plt.plot(X_rolling, y_rolling, c='black', label='Rolling average 60 min')

# science lol
# plt.plot(X1, (y1+y3+y4+y6)/5, c='black', label='super_average_metric')

plt.legend(loc='upper right')
plt.show()

