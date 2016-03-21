import pickle
import numpy as np
from sklearn import neighbors, metrics
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_predict
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
#pred_lr = model_lr.fit(X, y).predict(X)
pred_lr = cross_val_predict(model_lr, X, y, cv=10)

model_nn = neighbors.KNeighborsRegressor(5, weights='distance')
#pred_nn = model_nn.fit(X, y).predict(X)
pred_nn = cross_val_predict(model_nn, X, y, cv=10)

model_poly = make_pipeline(PolynomialFeatures(3), Ridge())
#pred_poly = model_poly.fit(X, y).predict(X)
pred_poly = cross_val_predict(model_poly, X, y, cv=10)

#print metrics.accuracy_score(y, pred_poly)
#print model_lr.score(X,y)
#print model_nn.score(X,y)
#print model_poly.score(X,y)

fig, ax = plt.subplots()
ax.scatter(y, pred_lr, c='g')
#ax.scatter(y, pred_rbf, c='g')
ax.scatter(y, pred_poly, c='b')
ax.scatter(y, pred_nn, c='y')
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
