from elastic_api.PresentButFinishedLoader import PresentButFinishedLoader
import time
import elastic_api.parse_date as parse_date
import numpy as np
import matplotlib.pyplot as plt
start_time = "2016-03-26 14:00"
end_time = "2016-03-26 16:00"
interval = 10

turbo = PresentButFinishedLoader(start_time, end_time, interval)

v = turbo.load_vector()

plt.plot(v)
plt.show()
