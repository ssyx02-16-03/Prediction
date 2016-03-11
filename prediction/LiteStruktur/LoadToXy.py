
import numpy as np
import pickle

from sklearn.datasets.base import Bunch

from TTTLoader import TTTLoader
from NbrOfPatientsLoader import NbrOfPatientsLoader

startTime = "2016-03-06 00:00"
endTime = "2016-03-07 00:00"
interval = 60

ttt = TTTLoader(startTime, endTime, interval)

numPats = NbrOfPatientsLoader(startTime, endTime, interval)

delayed_ttt = TTTLoader(startTime, endTime, interval)
delayed_ttt.set_offset(120)

x1 = ttt.load()
x2 = numPats.load()

X = np.column_stack([x1, x2])
y = delayed_ttt.load()

data = Bunch(data=X, target=y)

with open('data.pkl', 'w') as file:
    pickle.dump(data, file)
    file.close()
