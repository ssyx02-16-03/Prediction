# coding=utf-8
import matplotlib.pyplot as plt
import os

from sklearn import neighbors

from sklearn.preprocessing import PolynomialFeatures

from sklearn.pipeline import make_pipeline

from sklearn.linear_model import LassoCV, Ridge

import config
from elastic_api import parse_date
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

colors = ['blue', 'red', 'green', 'purple', 'yellow', 'pink']
start_time = "2016-04-06 12:00"
end_time = "2016-04-20 12:00"
end_time_min = (parse_date.date_to_millis(end_time) - parse_date.date_to_millis(start_time)) / 60000
X_plot = np.linspace(0, end_time_min-1, end_time_min/10)[:, np.newaxis]
num_models = 4
Xs = []
ys = []
model_place = config.saved_models_path
lasso = LassoCV()
mpl = MLPRegressor()
poly = make_pipeline(PolynomialFeatures(2), Ridge())
knn = neighbors.KNeighborsRegressor(5, weights='distance')
methods = [mpl, lasso, knn, poly]
m_names = ['Neural Network', 'LassoCV', 'KNN', 'Polynom']
type = 'TotalTime'
for i in range(0, num_models, 1):
    Xs.append(joblib.load(model_place + str(i * 10) + type + 'X.pkl'))
    ys.append(joblib.load(model_place + str(i * 10) + type + 'y.pkl'))

X_plot = X_plot[60:-120]
print str(type) + ': Antal mätpunkter: ' + str(X_plot.shape)
f, ax = plt.subplots(len(methods)/2, len(methods)/2)
for k in range(0,len(methods),1):
    #for i in range(0, num_models, 1):
    i = 3
    print 'testing model: ' + str(i*10)
    #pred = cross_val_score(method, Xs[i], ys[i], cv=10, verbose=True)
    #ax[i].scatter(i, sum(pred) / len(pred), label=str(i * 10), color=colors[k])
    X = Xs[i][60:-120]
    y = ys[i][60:-120]
    pred = cross_val_predict(methods[k], X, y, cv=10, verbose=True)
    temp_ax = ax[k/2, k%2]
    temp_ax.scatter(y, pred, label=m_names[k], color=colors[k], marker='+')
    #temp_ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=1)
    print 'mean squared error: ' + str(np.sqrt(mean_squared_error(y, pred)))
    temp_ax.plot(X_plot, pred, label=str(i), color=colors[i])
    temp_ax.legend(loc='upper left')
    #temp_ax.set_xlabel('Measured')
    #temp_ax.set_ylabel('Predicted')
plt.setp([a.set_xlabel('Measured') for a in ax[1, :]])
plt.setp([a.set_ylabel('Predicted') for a in ax[:, 0]])
plt.setp([a.get_yticklabels() for a in ax[:, 1]], visible=False)
plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)
plt.show()
