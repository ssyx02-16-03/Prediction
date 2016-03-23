from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
import time
import elastic_api.parse_date as parse_date
import numpy as np
import matplotlib.pyplot as plt

start_time = "2016-03-22 17:00"
end_time = "2016-03-23 17:00"
interval = 5

turbo = AverageTimeWaitedLoader(start_time, end_time, interval)
time_point = parse_date.date_to_millis(start_time)

print turbo.load_value(time_point, 60*60*1000)


v = turbo.load_vector()
print "go"

plt.plot(v)
plt.title(start_time + " to " + end_time)
plt.show()

print "done"