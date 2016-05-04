# coding=utf-8
import matplotlib.pyplot as plt
import os
import config
from elastic_api import parse_date
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

colors = ['blue', 'red', 'green', 'purple', 'yellow', 'pink']
start_time = "2016-04-16 12:00"
end_time = "2016-04-21 12:00"
end_time_min = (parse_date.date_to_millis(end_time) - parse_date.date_to_millis(start_time)) / 60000
X_plot = np.linspace(0, end_time_min-1, end_time_min)[:, np.newaxis]
num_models = 4
Xs = []
ys = []
model_place = config.saved_models_path

type = 'TimeToTriage'
for i in range(0, num_models, 1):
    Xs.append(joblib.load(model_place + str(i * 10) + type + 'X.pkl'))
    ys.append(joblib.load(model_place + str(i * 10) + type + 'y.pkl'))

X_plot = X_plot[60:-1200]
mpl = MLPRegressor()
for i in range(0, num_models, 1):
    print 'testing model: ' + str(i*10)
    #mpl_pred = cross_val_score(mpl, Xs[i], ys[i], cv=10, verbose=True)
    #plt.scatter(i, sum(mpl_pred)/len(mpl_pred), label=str(i*10), color=colors[i])
    X = Xs[i][60:-1200]
    y = ys[i][60:-1200]
    mpl_pred = cross_val_predict(mpl, X, y, cv=10, verbose=True)
    #plt.scatter(y, mpl_pred, label=str(i), color=colors[i], marker='x')
    print 'mean squared error: ' + str(mean_squared_error(y,mpl_pred))
    plt.plot(X_plot, mpl_pred, label=str(i), color=colors[i])
plt.legend(loc='best')
plt.show()
