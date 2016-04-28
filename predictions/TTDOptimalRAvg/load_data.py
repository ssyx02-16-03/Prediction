from WaitTimesPerPatient.TTD import TTD
import numpy as np


time1 = "2016-03-07 00:00"
time2 = "2016-04-18 00:00"

presentTTD = TTD(time1, time2)
seat_times = presentTTD.get_seat_time()
ttd = presentTTD.get_ttd()

np.savez('data', seat_times=seat_times, ttd=ttd)
