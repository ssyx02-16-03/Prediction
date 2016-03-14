import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn import linear_model

data = np.load("data.npz")
ttt = data['ttt']
reds = data['reds']
oranges = data['oranges']
futureTTT = data['futureTTT']

x1 = ttt
x2 = reds + oranges
x1x1 = x1 * x1
x1x2 = x1 * x2
x2x2 = x2 * x2
X = np.column_stack([x1, x2, x1x1, x1x2, x2x2])
y = futureTTT

regr = linear_model.LinearRegression()
regr.fit(X, y)

x1l = np.linspace(-500000, 3500000, num=100)
x2l = np.linspace(-5, 35, num=100)
x1v, x2v = np.meshgrid(x1l, x2l)
c = regr.coef_
zpol = c[0] * x1v +\
       c[1] * x2v +\
       c[2] * x1v * x1v +\
       c[3] * x1v * x2v +\
       c[4] * x2v * x2v

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = x1[:]
    ys = x2[:]
    zs = y[:]
    ax.scatter(xs, ys, zs, c=c, marker=m)
    ax.plot_surface(x1v, x2v, zpol)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
