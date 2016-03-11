import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.gaussian_process import GaussianProcess
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn import neighbors

with open('training.json') as jsonfile:
    points = json.load(jsonfile)['points']
    jsonfile.close()

X = []
y = []
for point in points:
    X.append(point['time'])
    y.append(point['count'])

X = np.asarray(X)
y = np.asarray(y)

with open('test.json') as testfile:
    testPoints = json.load(testfile)['points']
    testfile.close()
X_test = []
y_test = []
for point in testPoints:
    X_test.append(point['time'])
    y_test.append(point['count'])

X_test = np.asarray(X_test)
y_test = np.asarray(y_test)

x_plot = np.linspace(X[0], X[X.size-1], 300)
X = X[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]
X_test = X_test[:, np.newaxis]



'''
# create matrix versions of these arrays
y = np.asarray(y_t)
x = np.asarray(x_t)
X = x[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

print X.shape


plt.scatter(X, y, label="training points")
plt.scatter(X_test, y_test, label="test points", c='g')

for degree in [3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    print model.score(X_test, y_test)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='upper left')

plt.show()
'''
T=X_plot

for i, weights in enumerate(['uniform', 'distance']):
    plt.subplot(2, 1, i + 1)
    plt.scatter(X, y, c='k', label='data')
    for n_neighbors in [5, 10]:
        knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
        y_ = knn.fit(X, y).predict(T)
        plt.plot(T, y_, label=weights + str(n_neighbors))
        plt.axis('tight')
        plt.legend()
        plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors,
                                                                    weights))
plt.show()
'''
x = X_plot
gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
                     random_start=100)

gp.fit(X, y)
y_pred, MSE = gp.predict(X_plot, eval_MSE=True)
sigma = np.sqrt(MSE)
fig = plt.figure()
plt.plot(X, y, 'r.', markersize=10, label=u'Observations')
plt.plot(x, y_pred, 'b-', label=u'Prediction')
plt.fill(np.concatenate([x, x[::-1]]),
         np.concatenate([y_pred - 1.9600 * sigma,
                        (y_pred + 1.9600 * sigma)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
plt.ylim(-10, 20)
plt.legend(loc='upper left')
plt.show()
'''