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

    if wait_times == []:  # null check, triggers if nothing interesting happened on the interval
        return [], []

    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):
        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)

    X = (event_times-event_times[0])/60000
    X_plot = np.linspace(0, (X[len(X)-1])+60, 100)[:, np.newaxis]

    model = neighbors.KNeighborsRegressor(2, weights='distance')

    model.fit(X, wait_means)
    y = model.predict(X_plot)
    return X_plot, y
