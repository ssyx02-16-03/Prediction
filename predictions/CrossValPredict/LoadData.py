import numpy as np
import pickle

from sklearn.datasets.base import Bunch

from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from elastic_api.NewPatientsLoader import NewPatientsLoader
from elastic_api.OngoingsLoader import OngoingsLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
from elastic_api.UntriagedLoader import UntriagedLoader
from elastic_api.WaitTimeLoaders import TTTLoader

start_time = "2016-03-09 00:00"
end_time = "2016-03-11 00:00"
interval = 60

#ttt = TimeToEventLoader(start_time, end_time, interval)
#ttt.set_search_triage()
ttt = TTTLoader(start_time, end_time, interval)
ongoing = OngoingsLoader(start_time, end_time, interval)
newCount = NewPatientsLoader(start_time, end_time, interval)
mep = OngoingsLoader(start_time, end_time, interval)
avgWait = AverageTimeWaitedLoader(start_time, end_time, interval)
avgWait.set_search_triage()
unTri = UntriagedLoader(start_time, end_time, interval)
unTri.set_search_triage()
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
#futureTTT = TimeToEventLoader(start_time, end_time, interval)
#futureTTT.set_search_triage()
futureTTT.set_offset(60)

x1 = ongoing.get_times_of_day()
x2 = ongoing.load_vector()
x3 = newCount.load_value()
x4 = ttt.load_vector()
x5 = mep.load_vector()
#x6 = ttt2.load_vector()
#x6 = ongoing.get_weekdays()
x6 = avgWait.load_vector()
x7 = unTri.load_vector()


X = np.column_stack([x1, x2, x3, x4, x5, x6, x7])
y = futureTTT.load_vector()

print X
print y

data = Bunch(
        data=X,
        target=y)

with open('Xy.pkl', 'w') as file:
    pickle.dump(data, file)
    file.close()