# coding=utf-8
import matplotlib.pyplot as plt
import os

from sklearn import neighbors, linear_model, metrics

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

scores_list_a = []
scores_list_b = []
scores_list_c = []


def scores(a, b):
    scores_list_a.append(round(metrics.mean_absolute_error(a, b), 2))
    scores_list_b.append(round(metrics.median_absolute_error(a, b), 2))
    scores_list_c.append(round(np.std((np.abs(a - b))), 2))


def print_scores():
    for i in range(0, len(scores_list_a), 1):
        print '{} & {} & {} & {} & {}\% \\\\'.format(str(m_names[i][:3]), scores_list_a[i], scores_list_b[i],
                                                   scores_list_c[i], round(100 * scores_list_a[i] / y_mean, 1))


colors = ['blue', 'red', 'green', 'purple', 'yellow', 'orange']
model_place = config.saved_models_path
linear = linear_model.LinearRegression()
lassoCV = LassoCV()
mpl = MLPRegressor()
poly = make_pipeline(PolynomialFeatures(2), Ridge())
knn = neighbors.KNeighborsRegressor(5, weights='distance')
lasso = linear_model.Lasso(alpha=0.1, max_iter=100000)
methods = [mpl, lassoCV, linear, poly, knn]
m_names = [u'Neuralt Nätverk', 'Lasso', u'Linjär', 'Polynom', 'KNN', 'Q-Lasso']
type = 'ny'
X = joblib.load(model_place + type + 'X.pkl')
y = joblib.load(model_place + type + 'y.pkl')
y_mean = np.mean(y)

type = 'big'
Xbig = joblib.load(model_place + type + 'X.pkl')
ybig = joblib.load(model_place + type + 'y.pkl')

print lassoCV.fit(X, y).coef_
print Xbig.shape
print y_mean
f, ax = plt.subplots(3, 2)
for k in range(0, len(methods), 1):
    pred = cross_val_predict(methods[k], X, y, cv=10, verbose=True)
    temp_ax = ax[k / 2, k % 2]
    temp_ax.scatter(y, pred, marker='x', label=m_names[k], color=colors[1], alpha=0.15, s=1)
    temp_ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=1)
    scores(y, pred)
    temp_ax.legend(loc='upper left', fontsize=10)
    temp_ax.tick_params(labelsize=8)

pred = cross_val_predict(lasso, Xbig, ybig, cv=10, verbose=True)
k = 5
temp_ax = ax[2, 1]
temp_ax.scatter(ybig, pred, marker='x', label=m_names[k], color=colors[1], alpha=0.15, s=1)
temp_ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=1)
scores(y, pred)
temp_ax.legend(loc='upper left', fontsize=10)
plt.tick_params(labelsize=8)

print_scores()
plt.setp([a.set_xlabel(u'Uppmätt') for a in ax[2, :]])
plt.setp([a.set_ylabel('Predikterat') for a in ax[:, 0]])
plt.setp([a.get_yticklabels() for a in ax[:, 1]], visible=False)
plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)
plt.setp([a.get_xticklabels() for a in ax[1, :]], visible=False)
plt.suptitle(u'Tid till triage')
plt.tight_layout(h_pad=0.1, w_pad=0.05, rect=[0.1, 0, 0.85, 0.98])

plt.savefig('test.pdf')
