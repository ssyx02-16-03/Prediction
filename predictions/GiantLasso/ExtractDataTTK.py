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

fttk120 = data["future_time"]["future_ttk120"] / (1000 * 60)  # in minutes
y1 = time["rolling_ttk30"] / (1000 * 60)
y2 = workload["new60"]
y3 = capacity["speed_finished_60"]
y4 = workload["unfinished"]
y5 = data["unknown_dim"]["waited_finished"] / (1000 * 60)
y6 = time["rolling_ttk60"] / (1000 * 60)
y7 = time["rolling_ttk120"] / (1000 * 60)
#x1 = ttk nu
#x2 = ankomst tempo
#x3 = triage tempo
#x4 = otriagerade
#x5 = avg wait bland otriagerade
#x6 = ttk för 30 min sen
#x7 = ttk för 15 min sen
X = np.column_stack([y1, y2, y3, y4, y5, y6, y7])

i = 0
while i < len(fttk120):
    if not (1 < fttk120[i] < 800):  # removing unreasonable stuff...
        fttk120 = np.delete(fttk120, i, 0)
        X = np.delete(X, i, 0)
        i -= 1
    i += 1

joblib.dump(X, saved_models_path + 'nyX.pkl')
joblib.dump(fttk120, saved_models_path + 'nyy.pkl')