import numpy as np

from elastic_api.WaitTimeLoaders import TTTLoader
from elastic_api.ColorLoaders import RedsLoader, OrangesLoader

start_time = "2016-03-06 00:00"
end_time = "2016-03-13 00:00"
interval = 60

tttLoader = TTTLoader(start_time, end_time, interval)
redsLoader = RedsLoader(start_time, end_time, interval)
orangesLoader = OrangesLoader(start_time, end_time, interval)

times = tttLoader.get_times()
ttt = tttLoader.load_vector()
reds = redsLoader.load_vector()
oranges = orangesLoader.load_vector()

np.savez('data', times = times, ttt = ttt, reds = reds, oranges = oranges)