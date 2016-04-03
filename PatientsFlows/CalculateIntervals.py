import numpy as np
from scipy.integrate import simps

from elastic_api.TimeToEventLoader import TimeToEventLoader

start_time = "2016-03-22 12:00"
end_time = "2016-04-03 12:00"
interval = 60
percent_new = 0.1
percent_old = 1-percent_new

ttt = TimeToEventLoader(start_time, end_time, interval)
ttt.set_search_triage()

times = ttt.get_event_times()
ttt_times = np.column_stack(times)
ttt_times = ttt_times[np.argsort(ttt_times[:,0])]
arr_times = ttt_times[:,0]
tri_times = ttt_times[:,1]
#ttt_times = (ttt_times[:,1]-ttt_times[:,0])/60000
print ttt_times
arr_times = np.column_stack(arr_times)[0]
tri_times = np.column_stack(tri_times)[0]

ttt_means = []
ttt_mean = arr_times[0]-tri_times[0]
for i in range(0, len(arr_times), 1):
    ttt_mean = ttt_mean * percent_old + (tri_times[i]-arr_times[i]) * percent_new
    ttt_means.append(ttt_mean)

arr_times = arr_times[np.argsort(arr_times)]
arrivial_speeds=[]
arrivial_speeds.append(arr_times[1] - arr_times[0])
arrivial_speed = arr_times[1] - arr_times[0]
for i in range(0, len(arr_times)-1, 1):
    arrivial_speed = arrivial_speed * percent_old + (arr_times[i+1]-arr_times[i]) * percent_new
    arrivial_speeds.append(arrivial_speed)

tri_times = tri_times[np.argsort(tri_times)]
done_speeds=[]
done_speeds.append(tri_times[1] - tri_times[0])
done_speed = tri_times[1] - tri_times[0]
for i in range(0, len(tri_times)-1, 1):
    done_speed = done_speed * percent_old + (tri_times[i+1]-tri_times[i]) * percent_new
    done_speeds.append(done_speed)

arrivial_speeds = np.column_stack(arrivial_speeds)[0]/60000
done_speeds = np.column_stack(done_speeds)[0]/60000
ttt_means = np.column_stack(ttt_means)[0]/60000

import matplotlib.pyplot as plt
plt.plot((arr_times-arrivial_speeds[0])/60000, 60/arrivial_speeds)
plt.plot((tri_times-arrivial_speeds[0])/60000, 60/done_speeds)
plt.plot((arr_times-arrivial_speeds[0])/60000, ttt_means)
#plt.plot(arr_times, arrivial_speeds-done_speeds)

plt.show()
