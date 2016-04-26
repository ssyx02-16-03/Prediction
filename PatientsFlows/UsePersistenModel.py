# coding=utf-8
from PatientsFlows import RealTimeWait
from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from elastic_api.UntriagedLoader import UntriagedLoader
from sklearn import neighbors
import numpy as np
import matplotlib.pyplot as plt

from elastic_api.TimeToEventLoader import TimeToEventLoader
from sklearn.externals import joblib

colors = ['blue', 'red', 'green', 'purple', 'yellow']

#x1 = ttt nu
#x2 = ankomst tempo
#x3 = triage tempo
#x4 = otriagerade
#x5 = avg wait bland otriagerade
#x6 = ttt för 30 min sen
#x7 = ttt för 15 min sen

def predict_now(start_time, end_time):

    start_time_min = parse_date.date_to_millis(start_time)/60000-120
    end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000

    X_pred = []
    models = []
    for i in range(0, 4, 1):
        X_pred.append(end_time_min + i*10)
        models.append(joblib.load(str(i*10) + 'mpl.pkl'))

    interval = 1
    ttt = TimeToEventLoader(start_time, end_time, interval)
    ttt.set_search_triage()


    arr, tri, wait, real = RealTimeWait.moving_average(ttt)
    tri = np.asarray(tri)
    tri = tri/60000-start_time_min
    arr = np.asarray(arr)
    arr = arr/60000-start_time_min
    y2, y3 = RealTimeWait.get_speeds(ttt)

    X_plot = np.linspace(0, end_time_min, 24*60)[:, np.newaxis]

    model = neighbors.KNeighborsRegressor(5, weights='distance')
    model.fit(tri, wait)
    y1_p = model.predict(X_plot)

    model.fit(arr, y2)
    y2_p = model.predict(X_plot)
    model.fit(tri, y3)
    y3_p = model.predict(X_plot)

    start_time=end_time[:-2] + str(int(end_time[-2:])-interval)
    print start_time
    untriage = UntriagedLoader(start_time, end_time, interval)
    untriage.set_search_triage()
    y4 = untriage.load_vector()
    wait_loader = AverageTimeWaitedLoader(start_time, end_time, interval)
    wait_loader.set_search_triage()
    y5 = wait_loader.load_vector()/60000

    x1 = wait[-1]
    x2 = y2_p[-1]
    x3 = y3_p[-1]
    x4 = y4#[-30:-1]
    x5 = y5#_p[-30:-1]
    x6 = y1_p[-31]
    x7 = y1_p[-16]

    X = np.column_stack([x1, x2, x3, x4, x5, x6, x7])
    print X
    pred = []
    for i in range(0, 4, 1):
        print str(i*10)
        pred.append(models[i].predict(X)[0])
    return X_plot, pred, y1_p, X_pred


start_time = "2016-04-25 13:30"
end_time = "2016-04-26 13:30"
interval = 1

X_plot, pred, hist, X_pred = predict_now(start_time, end_time)

print pred, X_pred

plt.plot(X_plot, hist, c='blue')
plt.plot(X_pred, pred, c='yellow')
plt.show()
