from TTTNow.PresentTTT import PresentTTT
from elastic_api.UntriagedLoader import UntriagedLoader
import time
import numpy as np

time1 = "2016-03-08 10:00"
time2 = "2016-03-18 10:00"

presentTTT = PresentTTT(time1, time2)
seat_times = presentTTT.get_seat_time()
ttt = presentTTT.get_ttt()

untriagedLoader = UntriagedLoader(time1, time2, 0) # interval unused
untriageds = np.array([])
for time in seat_times:
    untriageds_value = int(untriagedLoader.load_value(int(time), 0)) # interval unused
    untriageds = np.append(untriageds, untriageds_value)

#millitime = int(time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M"))) * 1000

np.savez('data', untriageds = untriageds, ttt = ttt)


