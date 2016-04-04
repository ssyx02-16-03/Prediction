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

def run(start_time, end_time):

    ttt = TimeToEventLoader(start_time, end_time, 0)
    ttt.set_search_triage()

    times = ttt.get_event_times()
    ttt_times = np.column_stack(times)
    ttt_times = ttt_times[np.argsort(ttt_times[:,1])]
    arr_times = ttt_times[:,0]
    tri_times = ttt_times[:,1]
    ttt_times = (ttt_times[:,1]-ttt_times[:,0])/60000
    arr_times = np.asanyarray(arr_times)[:, np.newaxis]
    tri_times = np.asanyarray(tri_times)[:, np.newaxis]

    ttt_means = []
    ttt_mean = ttt_times[0]
    for i in range(0, len(tri_times), 1):
        ttt_mean = ttt_mean * percent_old + ttt_times[i] * percent_new
        ttt_means.append(ttt_mean)

    ttt_means = np.asarray(ttt_means)

    X = (tri_times-tri_times[0])/60000
    X_plot = np.linspace(0, (X[len(X)-1])+60, 100)[:, np.newaxis]

    model = neighbors.KNeighborsRegressor(2, weights='distance')

    model.fit(X, ttt_means)
    y = model.predict(X_plot)
    return X_plot, y
