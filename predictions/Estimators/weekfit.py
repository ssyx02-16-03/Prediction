# import cPickle
# import numpy as np
from predictions.Estimators.LWRegressor import LWRegressor
# import matplotlib.pyplot as plt


def weektime_feature(measurement_times, prediction_parameter):
    MILLIS_OF_WEEK = 7 * 24 * 60 * 60 * 1000
    week_millis = measurement_times % MILLIS_OF_WEEK
    lwreg = LWRegressor(90 * 60 * 1000)
    lwreg.fit(week_millis, prediction_parameter)
    return lwreg.predict(week_millis)

'''
# test
with open("data", "r") as file:
    data = cPickle.load(file)
    fttt120 = data["future_time"]["future_ttt120"]
    times = data["measurement_times"]

MILLIS_OF_WEEK = 7 * 24 * 60 * 60 * 1000
week_millis = times % MILLIS_OF_WEEK

plt.scatter(week_millis, fttt120, marker='x')

pred = weektime_feature(times, fttt120)
plt.scatter(week_millis, pred, c='red')

plt.show()
'''
