# problem: QL-article suggests varying window until a minimum is found,
# but in this computation MSE seems to monotonically increase
# will changing seat_times to treatment_times (as in article) fix it?
import numpy as np
import matplotlib.pyplot as plt
from predictions.Estimators.RAvgEstimator import RAvgEstimator


data = np.load('data.npz')
seat_times = data['seat_times'] / (1000 * 60)
ttd = data['ttd'] / (1000 * 60)  # in minutes

for vindov in range(15, 600 + 15, 15):
    # print seat_times[20] - seat_times[0]  # 450 minutes
    chop = 20  # removing points up to this index to not mess up estimator
    est = RAvgEstimator(window=vindov)
    est.fit(seat_times, ttd)
    ttd_pred = est.predict(seat_times[chop:])
    mse = ((ttd_pred - ttd[chop:]) ** 2).mean()
    print len(((ttd_pred - ttd[chop:]) ** 2))
    print "Mean square error with window of %d minutes is %f" % (vindov, mse)

plt.scatter(seat_times, ttd, marker='x')
plt.scatter(seat_times[chop:], ttd_pred, marker='x', c='red')
plt.show()
