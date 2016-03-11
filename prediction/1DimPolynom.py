import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


#data = None

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


x_plot = np.linspace(0, 1440, 100)
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
'''

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
