import pickle
import numpy as np
from sklearn import neighbors, metrics
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR

with open('/home/elin/Programming/git/Prediction/elastic_api/Xy.pkl', 'r') as input:
    dataset = pickle.load(input)
    input.close()

X=dataset.data
y=dataset.target

model_rbf = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5,
                   param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                               "gamma": np.logspace(-2, 2, 5)})
#model_rbf = SVR(C=1.0, epsilon=0.2)
pred_rbf = model_rbf.fit(X, y).predict(X)
#pred_rbf = cross_val_predict(model_rbf, X, y, cv=10)



model_lr = linear_model.LinearRegression()
#pred_lr = model_lr.fit(X, y).predict(X)
pred_lr = cross_val_predict(model_lr, X, y, cv=10)

model_nn = neighbors.KNeighborsRegressor(5, weights='distance')
pred_nn = model_nn.fit(X, y).predict(X)
#pred_nn = cross_val_predict(model_nn, X, y, cv=10)

model_poly = make_pipeline(PolynomialFeatures(3), Ridge())
#pred_poly = model_poly.fit(X, y).predict(X)
pred_poly = cross_val_predict(model_poly, X, y, cv=10)

print metrics.accuracy_score(y, pred_poly)
print model_lr.score(X,y)
print model_nn.score(X,y)
print model_poly.score(X,y)

fig, ax = plt.subplots()
ax.scatter(y, pred_lr, c='g')
ax.scatter(y, pred_poly, c='b')
ax.scatter(y, pred_nn, c='y')
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

'''
X_train=dataset.data[24:]
X_test=dataset.data[:24]
y_train=dataset.target[24:]
y_test=dataset.target[:24]

print X_train
print "...."
print X_test

alphas = np.logspace(-5, 1, 60)
enet = linear_model.ElasticNet(l1_ratio=0.7)
train_errors = list()
test_errors = list()
for alpha in alphas:
    enet.set_params(alpha=alpha)
    enet.fit(X_train, y_train)
    train_errors.append(enet.score(X_train, y_train))
    test_errors.append(enet.score(X_test, y_test))

i_alpha_optim = np.argmax(test_errors)
alpha_optim = alphas[i_alpha_optim]
print("Optimal regularization parameter : %s" % alpha_optim)


###############################################################################
# Plot results functions

import matplotlib.pyplot as plt
plt.semilogx(alphas, train_errors, label='Train')
plt.semilogx(alphas, test_errors, label='Test')
plt.vlines(alpha_optim, plt.ylim()[0], np.max(test_errors), color='k',
           linewidth=3, label='Optimum on test')
plt.legend(loc='lower left')
plt.xlabel('Regularization parameter')
plt.ylabel('Performance')
plt.show()

'''
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
ax.scatter(X[:, 0], X[:, 1], y)
ax.plot_wireframe(X[:, 0], X[:, 1], pred_poly)

ax.set_xlabel('TTT')
ax.set_ylabel('count')
ax.set_zlabel('TTT+2')

plt.show()
'''
