# import sys
# sys.path.append('/home/edvard/GitHub/Prediction')

import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # anvands!
import matplotlib.pyplot as plt
from sklearn import neighbors
from scipy.optimize import curve_fit
from sklearn.externals import joblib
import pickle
import cPickle

data = np.load('data.npz')
# untriageds = data['untriageds']
seat_times = data['seat_times']
weekdays = data['weekdays']
daytimes = data['daytimes'] / 3600  # i timmar
ttd = data['ttd']

x1 = weekdays
x2 = daytimes
# X = np.column_stack([x1, x2])  # shape (870, 2)!
X = x1 + 24 * x2
y = ttd

# plot av indata
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.scatter(x1, x2, y, c='r', marker='o')

# # nnfit och plot av nnfit
N = 100
x1l = np.ones(N)
x2l = np.linspace(0, 24, N)
Xl = np.column_stack([x1l, x2l])  # shape (100, 2)

xl = np.linspace(24, 24 * 8, N)  # till 1-dim

knn = neighbors.KNeighborsRegressor(n_neighbors=30, weights='uniform')
X.shape = (861,1)
y.shape = (861,1)
print X.shape, y.shape
knn = knn.fit(X, y)
xl.shape = (N,1)
print xl.shape
y_ = knn.predict(xl)

ax2 = fig.add_subplot(122)
ax2.plot(xl, y_)

plt.show()

# save the model
# joblib.dump(knn, 'model.pkl')
# pickle.dumps(knn)
with open('model.pkl', 'w') as file:
    cPickle.dump(knn, file)
