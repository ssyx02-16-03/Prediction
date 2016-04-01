import numpy as np

from elastic_api.TimeToEventLoader import TimeToEventLoader

start_time = "2016-03-24 11:00"
end_time = "2016-03-25 16:00"
interval = 60
percent_new = 0.2
percent_old = 1-percent_new

ttt = TimeToEventLoader(start_time, end_time, interval)
ttt.set_search_triage()

(arr_times, tri_times) = ttt.get_triage_times()

arr_times = np.column_stack(arr_times)[0]
tri_times = np.column_stack(tri_times)[0]
arr_times = arr_times[np.argsort(arr_times)]
tri_times = tri_times[np.argsort(tri_times)]
print arr_times
print tri_times

arrivial_speeds=[]
arrivial_speeds.append(arr_times[1] - arr_times[0])
arrivial_speed = arr_times[1] - arr_times[0]
for i in range(0, len(arr_times)-1, 1):
    arrivial_speed = arrivial_speed * percent_old + (arr_times[i+1]-arr_times[i]) * percent_new
    arrivial_speeds.append(arrivial_speed)

done_speeds=[]
done_speeds.append(tri_times[1] - tri_times[0])
done_speed = tri_times[1] - tri_times[0]
for i in range(0, len(tri_times)-1, 1):
    done_speed = done_speed * percent_old + (tri_times[i+1]-tri_times[i]) * percent_new
    done_speeds.append(done_speed)

import matplotlib.pyplot as plt

plt.plot(arr_times, arrivial_speeds)
plt.plot(tri_times, done_speeds)

plt.show()