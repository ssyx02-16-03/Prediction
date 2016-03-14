import numpy as np

from elastic_api.WaitTimeLoaders import TTTLoader
from elastic_api.ColorLoaders import RedsLoader, OrangesLoader

start_time = "2016-02-29 00:00"
end_time = "2016-03-14 00:00"
interval = 60

tttLoader = TTTLoader(start_time, end_time, interval)
redsLoader = RedsLoader(start_time, end_time, interval)
orangesLoader = OrangesLoader(start_time, end_time, interval)
futureTTTLoader = TTTLoader(start_time, end_time, interval)
futureTTTLoader.set_offset(60)

ttt = tttLoader.load_vector()
reds = redsLoader.load_vector()
oranges = orangesLoader.load_vector()
futureTTT = futureTTTLoader.load_vector()

np.savez('../predictions/ExplicitGeneralizedLinear/data',
         ttt = ttt, reds = reds, oranges = oranges, futureTTT = futureTTT)


