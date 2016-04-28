# coding=utf-8
import time

import config
from PatientsFlows import RealTimeWait
from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from elastic_api.UntriagedLoader import UntriagedLoader
from sklearn import neighbors
import numpy as np
import matplotlib.pyplot as plt

from elastic_api.TimeToEventLoader import TimeToEventLoader
from sklearn.externals import joblib
from predictions.Estimators.LWRegressor import LWRegressor

colors = ['blue', 'red', 'green', 'purple', 'yellow']

#x1 = ttt nu
#x2 = ankomst tempo
#x3 = triage tempo
#x4 = otriagerade
#x5 = avg wait bland otriagerade
#x6 = ttt för 30 min sen
#x7 = ttt för 15 min sen

num_models = 4
model_place = config.saved_models_path  #  '../SavedModels/'

# start_time and end_time should be in epoch millis
def predict_now(start_time, end_time, type):

    start_time_min = start_time/60000
    end_time_min = (end_time-start_time)/60000

    X_pred = []
    models = []
    for i in range(0, num_models, 1):
        X_pred.append(end_time_min + i*10)
        models.append(joblib.load(model_place + str(i*10) + 'mpl' + type + '.pkl'))

    interval = 1
    ttt = TimeToEventLoader(start_time, end_time, interval)
    ttt.set_event_name(type)


    arr, tri, wait, real = RealTimeWait.moving_average(ttt)
    tri = np.asarray(tri)
    tri = tri/60000-start_time_min
    arr, tri2, y2, y3 = RealTimeWait.get_speeds(ttt)
    arr = np.asarray(arr)
    arr = arr/60000-start_time_min
    tri2 = np.asarray(tri2)
    tri2 = tri2/60000-start_time_min

    X_plot = np.linspace(0, end_time_min, end_time_min + 1)[:, np.newaxis]

    model = neighbors.KNeighborsRegressor(5, weights='distance')
    model.fit(tri, wait)
    y1_p = model.predict(X_plot)

    model.fit(arr, y2)
    y2_p = model.predict(X_plot)
    model.fit(tri2, y3)
    y3_p = model.predict(X_plot)

    start_time = end_time - interval*1000*60
    #print start_time, end_time
    untriage = UntriagedLoader(start_time, end_time, interval)
    untriage.set_event_name(type)
    y4 = untriage.load_vector()
    wait_loader = AverageTimeWaitedLoader(start_time, end_time, interval)
    wait_loader.set_event_name(type)
    y5 = wait_loader.load_vector()/60000

    x1 = wait[-1]
    x2 = y2_p[-1]
    x3 = y3_p[-1]
    x4 = y4#[-30:-1]
    x5 = y5#_p[-30:-1]
    x6 = y1_p[-31]
    x7 = y1_p[-16]

    X = np.column_stack([x1, x2, x3, x4, x5, x6, x7])
    #print X
    pred = []
    for i in range(0, num_models, 1):
        #print str(i*10)
        pred.append(models[i].predict(X)[0])
    return tri, wait, X_pred, pred

def testing():
    start_time = int(time.mktime(time.strptime("2016-04-25 16:30", "%Y-%m-%d %H:%M"))) * 1000
    end_time = int(time.mktime(time.strptime("2016-04-26 20:07", "%Y-%m-%d %H:%M"))) * 1000

    X_plot, hist, X_pred, pred = predict_now(start_time, end_time, 'TotalTime')

    lwr = LWRegressor()
    lwr.fit(X_plot, hist)
    y = lwr.predict(X_plot)
    #print pred, X_pred

    plt.plot(X_plot, hist, c='blue')
    plt.plot(X_pred, pred, c='yellow')
    plt.show()
testing()
