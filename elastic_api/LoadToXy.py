import numpy as np
import pickle

from sklearn.datasets.base import Bunch

from WaitTimeLoaders import TTTLoader, TTDLoader
from ColorLoaders import RedsLoader, YellowsLoader, OrangesLoader, GreensLoader, BluesLoader
from TeamLoaders import NakbaLoader, NakkiLoader, NakkkLoader, NakmeLoader, NakmLoader, NakonLoader, NakorLoader
from OngoingsLoader import OngoingsLoader

start_time = "2016-03-07 00:00"
end_time = "2016-03-08 00:00"
interval = 60

oldRed = RedsLoader(start_time, end_time, interval)
oldRed.set_offset(-120)

ttt = TTTLoader(start_time, end_time, interval)
ongoing = OngoingsLoader(start_time, end_time, interval)
red = RedsLoader(start_time, end_time, interval)

futureTTT = TTTLoader(start_time, end_time, interval)
futureTTT.set_offset(120)

x1 = oldRed.load_vector()
x2 = ttt.load_vector()
x3 = ongoing.load_vector()
x4 = red.load_vector()

X = np.column_stack([x1, x2, x3, x4])
y = futureTTT.load_vector()

print X
print y

data = Bunch(data=X, target=y)

with open('Xy.pkl', 'w') as file:
    pickle.dump(data, file)
    file.close()