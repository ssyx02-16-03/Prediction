# coding=utf-8
import cPickle
import numpy as np

from PatientsFlows.config import saved_models_path
from sklearn.externals import joblib

with open("data", "r") as file:
    data = cPickle.load(file)

# these are column vectors
# these are dictionaries of column vectors
time = data["time"]
workload = data["workload"]
capacity = data["capacity"]

fttt120 = data["future_time"]["future_ttt120"] / (1000 * 60)  # in minutes
y1 = time["rolling_ttt30"] / (1000 * 60)
y2 = workload["new60"]
y3 = capacity["speed_triage_60"]
y4 = workload["untriaged"]
y5 = data["unknown_dim"]["waited_triage"] / (1000 * 60)
y6 = time["rolling_ttt60"] / (1000 * 60)
y7 = time["rolling_ttt120"] / (1000 * 60)
#x1 = ttt nu
#x2 = ankomst tempo
#x3 = triage tempo
#x4 = otriagerade
#x5 = avg wait bland otriagerade
#x6 = ttt för 30 min sen
#x7 = ttt för 15 min sen
X = np.column_stack([y1, y2, y3, y4, y5, y6, y7])

i = 0
while i < len(fttt120):
    if not (1 < fttt120[i] < 100):  # removing unreasonable stuff...
        fttt120 = np.delete(fttt120, i, 0)
        X = np.delete(X, i, 0)
        i -= 1
    i += 1

joblib.dump(X, saved_models_path + 'nyX.pkl')
joblib.dump(fttt120, saved_models_path + 'nyy.pkl')