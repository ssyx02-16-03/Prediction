# coding=utf-8
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.neural_network import MLPRegressor
import numpy as np

colors = ['blue', 'red', 'green', 'purple', 'yellow']
X_plot = np.linspace(0, 5*60*24, 5*60*24)[:, np.newaxis]

X = []
y = []
print 'hej'
for i in range(0, 4, 1):
    print str(i*10)
    X.append(joblib.load(str(i*10) + 'X.pkl'))
    y.append(joblib.load(str(i*10) + 'y.pkl'))


mpl = MLPRegressor()
for i in range(0, 4, 1):
    mpl_pred = cross_val_predict(mpl, X[i], y[i], cv=10, verbose=True)
    plt.plot(X_plot, mpl_pred, label=str(i), color=colors[i])
plt.legend(loc='best')
plt.show()
