import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

#data = None

with open('test.json') as jsonfile:
    points = json.load(jsonfile)['points']

X = []
y = []
for point in points:
    X.append(point['tid'])
    y.append(point['count'])

X = np.asarray(X)
y = np.asarray(y)

x_plot = np.linspace(0, 1440, 100)
X = X[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]



'''
# create matrix versions of these arrays
y = np.asarray(y_t)
x = np.asarray(x_t)
X = x[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

print X.shape
'''

plt.scatter(X, y, label="training points")

for degree in [3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='upper left')

#plt.show()


from sklearn.svm import SVR

# # Fit regression model
svr_rbf = SVR(kernel='rbf', degree=3, C=1e3)
y_rbf = svr_rbf.fit(X, y).predict(X)
plt.hold('on')
plt.plot(X, y_rbf, c='g', label='RBF model')
plt.show()