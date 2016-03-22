import numpy as np
import matplotlib.pyplot as plt

data = np.load('data.npz')
untriageds = data['untriageds']
ttt = data['ttt']

X = untriageds
y = ttt

print X.shape

plt.plot(X, y, 'ro')
axes = plt.gca()
axes.set_ylim([0, 10000000])
plt.show()