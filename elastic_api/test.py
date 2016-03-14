import numpy as np
import matplotlib.pyplot as plt

from OngoingsLoader import OngoingsLoader

start_time = "2015-09-01 00:00"
end_time = "2015-10-01 00:00"
interval = 60

inst = OngoingsLoader(start_time, end_time, interval)
#inst.set_team("NAKOR")
vector =  inst.load_vector()

x = np.arange(len(vector))

plt.plot(x, vector)

# plt.legend(loc='upper left')

plt.show()