import numpy as np
from sklearn import linear_model


def q(load_vec, rate_vec):
    q = np.array([])
    for i in range(len(load_vec)):
        q = np.append(q, load_vec[i].astype(float) / rate_vec[i].astype(float))
    return q

data = np.load('data.npz')
weektimes = data['weektimes']
ttd = data['ttd']
det_times = data['det_times']
t_waiters = data['t_waiters']
d_waiters = data['d_waiters']

# seems okay, perhaps all should be shape (N, 1) ...
print weektimes.shape
print ttd.shape
print det_times.shape
print t_waiters.shape
print d_waiters.shape

# transform attributes into q_features according to article
q_features = "hej hej paw dig min bror"  # TODO

# lasso
lasso = linear_model.Lasso(alpha=1.0)  # TODO decide nice alpha
lasso.fit(q_features, ttd)
