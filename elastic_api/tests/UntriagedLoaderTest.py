from elastic_api.UntriagedLoader import UntriagedLoader
import time
import elastic_api.parse_date as parse_date
import numpy as np
import matplotlib.pyplot as plt

start_time = "2016-03-22 00:00"
end_time = "2016-03-23 00:00"
interval = 5
time_point = parse_date.date_to_millis(start_time)

turbo = UntriagedLoader(start_time, end_time, interval)
turbo.set_search_triage()

print turbo.load_value(time_point, 60*60*1000)
v = turbo.load_vector()

plt.plot(v)
plt.show()
