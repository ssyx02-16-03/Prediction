# import sys
# sys.path.append('/home/edvard/GitHub/Prediction')

import numpy as np
import matplotlib.pyplot as plt

data = np.load('data.npz')
# untriageds = data['untriageds']
seat_times = data['seat_times']
ttt = data['ttt']

# X = untriageds
X = seat_times
y = ttt

print X.shape

plt.plot(X, y, 'ro')
axes = plt.gca()
axes.set_ylim([0, 10000000])
plt.show()
