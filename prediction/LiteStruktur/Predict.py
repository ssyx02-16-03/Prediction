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

with open('data.pkl', 'r') as input:
    dataset = pickle.load(input)
    input.close()
X = dataset.data
y = dataset.target
print(X)
print(y)

lr = neighbors.KNeighborsRegressor(5, weights='uniform')
predicted = cross_val_predict(lr, X, y, cv=10)

degree = 4
model = make_pipeline(PolynomialFeatures(degree), Ridge())
model.fit(X, y)
y_plot = model.predict(X)

fig, ax = plt.subplots()
ax.scatter(y, predicted)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
ax.scatter(X[:, 0], X[:, 1], y)
ax.plot_wireframe(X[:, 0], X[:, 1], y_plot)

ax.set_xlabel('TTT')
ax.set_ylabel('count')
ax.set_zlabel('TTT+2')

plt.show()
'''