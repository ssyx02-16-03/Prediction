import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

data = np.load("data.npz")
times = data["times"]
ttt = data["ttt"]

# Fouriertermer, antagen periodicitet en vecka
week_millis = 1000 * 60 * 60 * 24 * 7
x1 = np.cos((2 * np.pi / week_millis) * 1 * times)
x2 = np.cos((2 * np.pi / week_millis) * 2 * times)
x3 = np.cos((2 * np.pi / week_millis) * 3 * times)
x4 = np.cos((2 * np.pi / week_millis) * 4 * times)
x5 = np.cos((2 * np.pi / week_millis) * 5 * times)
x6 = np.cos((2 * np.pi / week_millis) * 6 * times)
x7 = np.cos((2 * np.pi / week_millis) * 7 * times)

X = np.column_stack([x1, x2, x3, x4, x5, x6, x7])
y = ttt

regr = linear_model.LinearRegression()
regr.fit(X, y)
c = regr.coef_

ypred = c[0] * np.cos((2 * np.pi / week_millis) * 1 * times) +\
    c[1] * np.cos((2 * np.pi / week_millis) * 2 * times) +\
    c[2] * np.cos((2 * np.pi / week_millis) * 3 * times) +\
    c[3] * np.cos((2 * np.pi / week_millis) * 4 * times) +\
    c[4] * np.cos((2 * np.pi / week_millis) * 5 * times) +\
    c[5] * np.cos((2 * np.pi / week_millis) * 6 * times) +\
    c[6] * np.cos((2 * np.pi / week_millis) * 7 * times)

plt.plot(times, ttt, 'ro')
plt.plot(times, ypred * 5 + 1000000)
plt.show()