import numpy as np
import pickle

from sklearn.datasets.base import Bunch

from WaitTimeLoaders import TTTLoader, TTDLoader
from ColorLoaders import RedsLoader, YellowsLoader, OrangesLoader, GreensLoader, BluesLoader
from TeamLoaders import NakbaLoader, NakkiLoader, NakkkLoader, NakmeLoader, NakmLoader, NakonLoader, NakorLoader
from OngoingsLoader import OngoingsLoader
from NewPatientsLoader import NewPatientsLoader
from TimeToEventLoader import TimeToEventLoader

start_time = "2016-03-09 00:00"
end_time = "2016-03-13 00:00"
interval = 120

ttt = TimeToEventLoader(start_time, end_time, interval)
ttt.set_search_triage()
ongoing = OngoingsLoader(start_time, end_time, interval)
newCount = NewPatientsLoader(start_time, end_time, interval)
mep = OngoingsLoader(start_time, end_time, interval)
mep.set_match({"filtered" : {
    "filter": {
        "bool": {
            "must": {
                "or": [
                    {
                        "match" : {"ReasonForVisit" :"MEP"}
                    },
                    {
                        "match" : {"ReasonForVisit" :"TRAU"}
                    }
                ]
            }
        }
    }
}})


futureTTT = TTTLoader(start_time, end_time, interval)
futureTTT.set_offset(120)

x1 = ongoing.get_times_of_day()
x2 = ongoing.load_vector()
x3 = newCount.load_value()
x4 = ttt.load_vector()
x5 = mep.load_vector()

X = np.column_stack([x1, x2, x3, x4, x5])
y = futureTTT.load_vector()

print X
print y

data = Bunch(
        data=X,
        target=y)

with open('Xy.pkl', 'w') as file:
    pickle.dump(data, file)
    file.close()