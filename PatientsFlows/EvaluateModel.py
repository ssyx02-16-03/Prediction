# coding=utf-8
import matplotlib.pyplot as plt
import os

from elastic_api import parse_date
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.neural_network import MLPRegressor
import numpy as np

colors = ['blue', 'red', 'green', 'purple', 'yellow', 'pink']
start_time = "2016-04-11 12:00"
end_time = "2016-04-21 12:00"
end_time_min = (parse_date.date_to_millis(end_time) - parse_date.date_to_millis(start_time)) / 60000
X_plot = np.linspace(0, end_time_min-1, end_time_min)[:, np.newaxis]
num_models = 4
Xs = []
ys = []
model_place = '../SavedModels/'

type = 'TimeToTriage'
for i in range(0, num_models, 1):
    Xs.append(joblib.load(model_place + str(i * 10) + type + 'X.pkl'))
    ys.append(joblib.load(model_place + str(i * 10) + type + 'y.pkl'))


mpl = MLPRegressor()
for i in range(0, num_models, 1):
    print 'testing model: ' + str(i*10)
    mpl_pred = cross_val_score(mpl, Xs[i], ys[i], cv=10, verbose=True)
    plt.scatter(i, sum(mpl_pred)/len(mpl_pred), label=str(i*10), color=colors[i])
    print mpl_pred.score()
    #mpl_pred = cross_val_predict(mpl, Xs[i], ys[i], cv=10, verbose=True)
    #plt.scatter(ys[i], mpl_pred, label=str(i), color=colors[i], marker='x')
    #plt.plot(X_plot, mpl_pred, label=str(i), color=colors[i])
plt.legend(loc='best')
plt.show()
