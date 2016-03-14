import numpy as np

from elastic_api.WaitTimeLoaders import TTTLoader

start_time = "2016-03-06 00:00"
end_time = "2016-03-13 00:00"
interval = 60

tttLoader = TTTLoader(start_time, end_time, interval)

times = tttLoader.get_times()
ttt = tttLoader.load_vector()

np.savez('data', times = times, ttt = ttt)