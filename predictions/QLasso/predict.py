import cPickle
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict
from sklearn.svm import SVR
import matplotlib.pyplot as plt


with open("data", "r") as file:
    data = cPickle.load(file)

# these are column vectors
fttt60 = data["fttt60"] / (1000 * 60)  # in minutes
# these are dictionaries of column vectors
time = data["time"]
workload = data["workload"]
capacity = data["capacity"]

# X = time["det_times"]
rttt30 = time["rttt30"] / (1000 * 60)
# X = np.hstack((X, rttt30))
X = rttt30
rttt60 = time["rttt60"] / (1000 * 60)
X = np.hstack((X, rttt60))

# transform attributes into Q features
Q = {}
for wl_key in workload:
    for cap_key in capacity:
        q_key = wl_key + ", " + cap_key
        for i in range(len(capacity[cap_key])):
            if capacity[cap_key][i] == 0:
                capacity[cap_key][i] = 1
        Q[q_key] = workload[wl_key] / capacity[cap_key]

for q_key in Q:
    X = np.hstack((X, Q[q_key]))

XX = X * X
# XXX = X * X * X
X = np.hstack((X, XX))  # X done

print X.shape
i = 0
while i < len(fttt60):
    if not (1 < fttt60[i] < 100):  # removing unreasonable stuff...
        # fttt60[i] = 20
        fttt60 = np.delete(fttt60, i, 0)
        X = np.delete(X, i, 0)
        i -= 1
    i += 1
print X.shape
y = fttt60  # y done

X_fit = X[:-300]
y_fit = y[:-300]
X_test = X[-300:]
y_test = y[-300:]

lasso = linear_model.LassoCV(max_iter=100000)

y_pred = cross_val_predict(lasso, X, y, verbose=True, cv=10)

plt.scatter(y, y_pred, marker='+')
plt.show()


lasso.fit(X_fit, y_fit)
print lasso
print lasso.coef_
#y_pred = lasso.predict(X_test)
MSE = np.mean((y_pred - y_test) ** 2)
STDEV = np.sqrt(MSE)
print STDEV

# kass.
# svr = SVR(kernel='rbf', C=1e2, gamma=1e0)
# svr.fit(X_fit[:,:9], y_fit.ravel())
# y_svr = svr.predict(X_test[:,:9])

#plt.plot(y_test, y_test)
#plt.scatter(y_test, y_pred, marker='x', c='b')
# plt.scatter(y_test, y_svr, marker='x', c='r')
# plt.axis([0, 50, 0, 50])
plt.show()
