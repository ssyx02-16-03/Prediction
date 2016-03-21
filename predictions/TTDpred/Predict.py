import pickle
import numpy as np
from sklearn import neighbors, metrics
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_predict, cross_val_score
from sklearn import linear_model
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR

with open('Xy.pkl', 'r') as input:
    dataset = pickle.load(input)
    input.close()

X=dataset.data
y=dataset.target


model_lr = linear_model.LinearRegression()
pred_lr = cross_val_predict(model_lr, X, y, cv=10)/6000
score_lr = cross_val_score(model_lr, X, y, cv=10)


model_nn = neighbors.KNeighborsRegressor(10, weights='distance')
pred_nn = cross_val_predict(model_nn, X, y, cv=10)/6000
score_nn = cross_val_score(model_nn, X, y, cv=10)

model_poly = make_pipeline(PolynomialFeatures(3), Ridge())
pred_poly = cross_val_predict(model_poly, X, y, cv=10)/6000
score_poly = cross_val_score(model_poly, X, y, cv=10)

y = y/6000

fig, ax = plt.subplots()
ax.scatter(y, pred_lr, c='g')
#ax.scatter(y, pred_poly, c='b')
ax.scatter(y, pred_nn, c='y')
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

x_plot = np.linspace(1, 10, 10)

plt.plot(x_plot, score_poly)
plt.plot(x_plot, score_nn)
plt.plot(x_plot, score_lr)
plt.show()

