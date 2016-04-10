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

def run(loader):

    times = loader.get_event_times()
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:,1])]
    arr_times = both_times[:,0]
    event_times = both_times[:,1]
    wait_times = (both_times[:,1]-both_times[:,0])/60000
    arr_times = np.asanyarray(arr_times)[:, np.newaxis]
    event_times = np.asanyarray(event_times)[:, np.newaxis]

    X_plot = np.linspace(loader.start_time, loader.end_time, 300)[:, np.newaxis]

    if len(wait_times) == 0:  # null check, triggers if nothing interesting happened on the interval
        return [X_plot], [np.linspace(0, 0, 300)]

    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):
        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)

    X = event_times

    model = neighbors.KNeighborsRegressor(5, weights='distance')

    model.fit(X, wait_means)
    try:
        y = model.predict(X_plot)
    except ValueError:
        y = np.linspace(0, 0, 300)

    return X_plot, y
