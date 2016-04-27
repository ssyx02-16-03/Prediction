import numpy as np
import matplotlib.pyplot as plt
from predictions.Estimators.LWRegressor import LWRegressor
import cPickle

data = np.load('data.npz')
# untriageds = data['untriageds']
seat_times = data['seat_times']
weekdays = data['weekdays']
daytimes = data['daytimes'] / 60  # i minuter
ttd = data['ttd'] / (1000 * 60)  # i minuter
print ttd

x1 = weekdays.reshape(-1, 1)
x2 = daytimes.reshape(-1, 1)
X = x1 * 24 * 60 + x2
y = ttd

xl = np.linspace(24 * 60, 24 * 8 * 60, 100).reshape(-1, 1)

lwReg = LWRegressor(sigma=120.0)
lwReg.fit(X, y)
y_pred = lwReg.predict(xl)

plt.scatter(X, y, marker='x')
plt.plot(xl, y_pred, c='red')
plt.show()

with open('model.pkl', 'w') as file:
    cPickle.dump(lwReg, file)
