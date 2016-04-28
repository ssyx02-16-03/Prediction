import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

from sklearn import linear_model, neighbors
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from elastic_api.TimeToEventLoader import TimeToEventLoader


percent_new = 0.1
percent_old = 1-percent_new


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
    percent_new = 0.1
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
    X_plot = np.linspace(loader.start_time, loader.end_time, 300)[:, np.newaxis]

    if not wait_times.any():  # null check, triggers if nothing interesting happened on the interval
        return [X_plot], [np.linspace(0, 0, 300)]
    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):
        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)
    return arr_times, event_times, wait_means, wait_times


def get_speeds(loader):

    times = loader.get_event_times()
    times = filter_zeroes(times) # filter out all zero event times. (patient was never even in the queue)
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:,1])]
    arr_times = both_times[:,0]
    event_times = both_times[:,1]

    arr_times = arr_times[np.argsort(arr_times)]
    arrivial_speeds=[]
    arrivial_speeds.append(arr_times[1] - arr_times[0])
    arrivial_speed = arr_times[1] - arr_times[0]
    for i in range(0, len(arr_times)-1, 1):
        arrivial_speed = arrivial_speed * percent_old + (arr_times[i+1]-arr_times[i]) * percent_new
        arrivial_speeds.append(arrivial_speed)

    tri_times = event_times[np.argsort(event_times)]
    done_speeds=[]
    done_speeds.append(tri_times[1] - tri_times[0])
    done_speed = tri_times[1] - tri_times[0]
    for i in range(0, len(tri_times)-1, 1):
        done_speed = done_speed * percent_old + (tri_times[i+1]-tri_times[i]) * percent_new
        done_speeds.append(done_speed)
    arrivial_speeds = np.asarray(arrivial_speeds)
    done_speeds = np.asarray(done_speeds)
    arr_times = np.asanyarray(arr_times)[:, np.newaxis]
    event_times = np.asanyarray(event_times)[:, np.newaxis]
    return arr_times, event_times, arrivial_speeds/60000, done_speeds/60000

