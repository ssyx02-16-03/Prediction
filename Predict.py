import pickle
import numpy as np
from sklearn import neighbors
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR

with open('/home/elin/Programming/git/Prediction/elastic_api/Xy.pkl', 'r') as input:
    dataset = pickle.load(input)
    input.close()
X = dataset.data
y = dataset.target
print(X)
print(y)

model_rbf = SVR(C=1.0, epsilon=0.2)
pred_rbf = model_rbf.fit(X, y).predict(X)

model_nn = neighbors.KNeighborsRegressor(5, weights='uniform')
pred_nn = model_nn.fit(X, y).predict(X)

degree = 3
model_poly = make_pipeline(PolynomialFeatures(degree), Ridge())
pred_poly = model_poly.fit(X, y).predict(X)

print model_nn.score(X,y)
print model_poly.score(X,y)

fig, ax = plt.subplots()
ax.scatter(y, pred_poly, c='b')
ax.scatter(y, pred_nn, c='y')
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
ax.scatter(X[:, 0], X[:, 1], y)
ax.plot_wireframe(X[:, 0], X[:, 1], pred_poly)

ax.set_xlabel('TTT')
ax.set_ylabel('count')
ax.set_zlabel('TTT+2')

plt.show()
'''