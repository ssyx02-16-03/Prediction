import cPickle
import numpy as np

from PatientsFlows.config import saved_models_path
from sklearn.externals import joblib

from sklearn import linear_model, metrics
# from sklearn.svm import SVR
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


with open("data", "r") as file:
    data = cPickle.load(file)

# these are column vectors
fttt120 = data["future_time"]["future_ttt120"] / (1000 * 60)  # in minutes
# these are dictionaries of column vectors
time = data["time"]
workload = data["workload"]
capacity = data["capacity"]

# X = time["det_times"]
wt = data["unknown_dim"]["waited_triage"]
wd = data["unknown_dim"]["waited_doctor"]
X = np.hstack((wt, wd))

for t_key in time:
    X = np.hstack((X, time[t_key] / (1000 * 60)))

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

print X.shape
i = 0
while i < len(fttt120):
    if not (1 < fttt120[i] < 100):  # removing unreasonable stuff...
        fttt120 = np.delete(fttt120, i, 0)
        X = np.delete(X, i, 0)
        i -= 1
    i += 1
print X.shape
y = fttt120  # y done

#X = X + X ** 2

# X = X[:, :20]
# X = PolynomialFeatures(2).fit_transform(X)
print X.shape

#X = X[:1000, :]
#y = y[:1000]

X_fit = X[:-100]
y_fit = y[:-100]
X_test = X[-100:]
y_test = y[-100:]

joblib.dump(X, saved_models_path + 'bigX.pkl')
joblib.dump(fttt120, saved_models_path + 'bigy.pkl')

lasso = linear_model.Lasso(alpha=0.1, max_iter=100000)
lasso.fit(X_fit, y_fit)
print lasso.coef_
y_pred = cross_val_predict(lasso, X, y, verbose=True, cv=10)
MSE = np.mean((y_pred - y_test) ** 2)
STDEV = np.sqrt(MSE)
print STDEV
print metrics.mean_absolute_error(y, y_pred)

#plt.scatter(y, y_pred, marker='+')
#plt.show()
#y_pred = lasso.predict(X_test)

# kass.
# svr = SVR(kernel='rbf', C=1e2, gamma=1e0)
# svr.fit(X_fit[:,:9], y_fit.ravel())
# y_svr = svr.predict(X_test[:,:9])

#plt.plot(y_test, y_test)
#plt.scatter(y_test, y_pred, marker='x', c='b')
# plt.scatter(y_test, y_svr, marker='x', c='r')
# plt.axis([0, 50, 0, 50])
#plt.show()
