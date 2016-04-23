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

poly = joblib.load('poly.pkl')
mpl = joblib.load('mpl.pkl')

start_time = "2016-04-24 15:30"
end_time = "2016-04-25 15:30"
interval = 1

start_time_min = parse_date.date_to_millis(start_time)/60000-120
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000

ttt = TimeToEventLoader(start_time, end_time, 0)
ttt.set_search_triage()
arr, tri, wait, real = RealTimeWait.moving_average(ttt)
tri = np.asarray(tri)
tri = tri/60000-start_time_min
arr = np.asarray(arr)
arr = arr/60000-start_time_min
y2, y3 = RealTimeWait.get_speeds(ttt)

X_plot = np.linspace(0, end_time_min, 24*60)[:, np.newaxis]

model = neighbors.KNeighborsRegressor(5, weights='distance')
#model = make_pipeline(PolynomialFeatures(10), Ridge())
model.fit(tri, wait)
y1_p = model.predict(X_plot)

model.fit(arr, y2)
y2_p = model.predict(X_plot)
model.fit(tri, y3)
y3_p = model.predict(X_plot)

start_time = "2016-03-30 11:30"
end_time = "2016-03-30 12:00"
untriage = UntriagedLoader(start_time, end_time, interval)
untriage.set_search_triage()
y4 = untriage.load_vector()
#X4 = untriage.get_times()[:, np.newaxis]
#X4 = (X4/60000-start_time_min)

wait_loader = AverageTimeWaitedLoader(start_time, end_time, interval)
wait_loader.set_search_triage()
y5 = wait_loader.load_vector()/60000
#X5 = wait_loader.get_times()[:, np.newaxis]
#X5 = (X5/60000-start_time_min)

#model.fit(X4, y4)
#y4_p = model.predict(X_plot)
#model.fit(X5, y5)
#y5_p = model.predict(X_plot)


x1 = wait[-31:-1]
x2 = y2_p[-31:-1]
x3 = y3_p[-31:-1]
x4 = y4#[-30:-1]
x5 = y5#_p[-30:-1]
x6 = y1_p[-61:-31]
x7 = y1_p[-46:-16]

X = np.column_stack([x1, x2, x3, x4, x5, x6, x7])
print X
#x1 = ttt nu
#x2 = ankomst tempo
#x3 = triage tempo
#x4 = otriagerade
#x5 = avg wait bland otriagerade
#x6 = ttt för 30 min sen
#x7 = ttt för 15 min sen


mpl_pred = mpl.predict(X)
poly_pred = poly.predict(X)

plt.plot(X_plot, y1_p, c='blue')
plt.plot(tri, wait, c='yellow')
plt.scatter(tri, real, marker='x', color='black')
#X_plot = np.linspace(end_time_min-30, end_time_min, 30)[:, np.newaxis]
#for i in range(0, len(X[0])-1, 1):
#    plt.plot(X_plot, X[:,i], label=i)
#plt.legend()
X_plot = np.linspace(end_time_min, end_time_min + 30, 30)[:, np.newaxis]
plt.plot(X_plot, mpl_pred, c='red')
plt.plot(X_plot, poly_pred, c='green')

plt.show()
