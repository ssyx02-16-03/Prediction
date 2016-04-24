# import sys
# sys.path.append('/home/edvard/GitHub/Prediction')

from WaitTimesPerPatient.TTD import TTD
# from elastic_api.UntriagedLoader import UntriagedLoader
# import time
import numpy as np

time1 = "2016-03-07 00:00"
time2 = "2016-04-18 00:00"

presentTTD = TTD(time1, time2)
seat_times = presentTTD.get_seat_time()
ttd = presentTTD.get_ttd()
weekdays = presentTTD.get_weekdays()
daytimes = presentTTD.get_daytimes()
print daytimes

# untriagedLoader = UntriagedLoader(time1, time2, 0) # interval unused
# untriageds = np.array([])
# for time in seat_times:
#     untriageds_value = int(untriagedLoader.load_value(int(time), 0)) # interval unused
#     untriageds = np.append(untriageds, untriageds_value)

# millitime = int(time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M"))) * 1000

np.savez('data', seat_times=seat_times, weekdays=weekdays, daytimes=daytimes, ttd=ttd)
