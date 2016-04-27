import numpy as np
from scipy.ndimage.interpolation import shift

import RealTimeWait
import config
from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from sklearn import neighbors
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib

from elastic_api.TimeToEventLoader import TimeToEventLoader
from elastic_api.UntriagedLoader import UntriagedLoader


model_place = config.saved_models_path#'../SavedModels/'
start_time = "2016-04-11 12:00"
end_time = "2016-04-21 12:00"
interval = 10
start_time_min = parse_date.date_to_millis(start_time) / 60000
end_time_min = (parse_date.date_to_millis(end_time) - parse_date.date_to_millis(start_time)) / 60000
X_plot = np.linspace(0, end_time_min, end_time_min  + 1)[:, np.newaxis]
print X_plot


def get_uniform_axes(X, y, method):
    method.fit(X, y)
    return method.predict(X_plot)


def fit_and_save_model(model, X_, y_, mins, name, type):
    model.fit(X_, y_)
    joblib.dump(model, model_place + str(mins) + name + type + '.pkl')


def save_data(X, y, min_shift, type):
    joblib.dump(X, model_place + str(min_shift) + type + 'X.pkl')
    joblib.dump(y, model_place + str(min_shift) + type + 'y.pkl')


def create_model(max_shift, type):
    print 'Creating ' + type + ' models for up to ' + str(max_shift) + ' minutes'
    ttt = TimeToEventLoader(start_time, end_time, 0)
    ttt.set_event_name(type)
    arr, tri, wait, real = RealTimeWait.moving_average(ttt)
    tri = np.asarray(tri)
    tri = tri / 60000 - start_time_min
    arr = np.asarray(arr)
    arr = arr / 60000 - start_time_min
    speed_arr, speed_tri = RealTimeWait.get_speeds(ttt)
    untriage = UntriagedLoader(start_time, end_time, interval)
    untriage.set_event_name(type)
    y4 = untriage.load_vector()
    X4 = untriage.get_times()[:, np.newaxis]
    X4 = (X4 / 60000 - start_time_min)

    wait_loader = AverageTimeWaitedLoader(start_time, end_time, interval)
    wait_loader.set_event_name(type)
    y5 = wait_loader.load_vector() / 60000
    X5 = wait_loader.get_times()[:, np.newaxis]
    X5 = (X5 / 60000 - start_time_min)

    print 'All data picked up, transforming it to uniform axes'
    model = neighbors.KNeighborsRegressor(5, weights='distance')
    y1 = get_uniform_axes(tri, wait, model)
    y2 = get_uniform_axes(arr, speed_arr, model)
    y3 = get_uniform_axes(tri, speed_tri, model)
    y4 = get_uniform_axes(X4, y4, model)
    y5 = get_uniform_axes(X5, y5, model)
    y6 = shift(y1, 30, cval=0)
    y7 = shift(y1, 15, cval=0)

    X = np.column_stack([y1, y2, y3, y4, y5, y6, y7])
    ys = []
    mpl = MLPRegressor()
    for i in range(0, max_shift + 1, 10):
        print i
        y = (shift(y1, -i, cval=0))
        #save_data(X, y, i, type)
        ys.append(y)
        fit_and_save_model(mpl, X, y, i, 'mpl', type)


create_model(60, 'TimeToTriage')
create_model(60, 'TimeToDoctor')
create_model(60, 'TotalTime')
