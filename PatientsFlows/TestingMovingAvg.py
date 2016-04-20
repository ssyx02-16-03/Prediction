import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift

from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from sklearn import neighbors
from sklearn.cross_validation import cross_val_predict, cross_val_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPRegressor

from elastic_api.TimeToEventLoader import TimeToEventLoader
from elastic_api.UntriagedLoader import UntriagedLoader

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

    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):
        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)

    X = (event_times-event_times[0])/60000
    return X, wait_means, wait_times

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

start_time = "2016-03-27 08:00"
end_time = "2016-03-28 08:00"
interval = 60
start_time_min = parse_date.date_to_millis(start_time)/60000
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000

ttt = TimeToEventLoader(start_time, end_time, interval)
ttt.set_search_triage()

#X_plot = np.linspace(0, end_time_min, 24*60)[:, np.newaxis]
X1, y1, y2 = run(ttt)
y3 = np.convolve(y2, np.ones((10,))/10, mode='same')
y4 = np.convolve(y2, np.ones((30,))/30, mode='same')
y5 = ttt.load_vector()/60000
X2 = ttt.get_times()[:, np.newaxis]
X2 = (X2/60000-start_time_min)+interval*2

y6 = ExpMovingAverage(y2, 10)


plt.plot(X1, y1, c='blue', label='10% nya')
plt.scatter(X1, y2, c='black', marker='x', label='Faktiska TTT-tider')
plt.plot(X1, y3, c='cyan', label='Glidande 10p')
plt.plot(X1, y4, c='green', label='Glidande 30p')
plt.plot(X2, y5, c='purple', label='60 min medel')
plt.plot(X1, y6, c='orange', label='Exp glidande 10p')
plt.legend(loc='upper right')
plt.show()

