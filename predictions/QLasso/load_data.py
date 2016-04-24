import numpy as np
from WaitTimesPerPatient.TTD import TTD
from elastic_api.UntriagedLoader import UntriagedLoader
import cPickle


def load_state_nbrs(times, loader):
    """
    use loader to get values of quantiative state variable at times
    lots of time wasted inside of this one apparently...
    """
    i = 1
    nbrs = np.array([])
    for timee in times:
        i = i + 1
        if i % 20 == 0:
            print i
        nbrs = np.append(nbrs, t_waiters_loader.load_value(timee, 0))
    return nbrs

time1 = "2016-03-07 00:00"
#time2 = "2016-03-14 00:00"
time2 = "2016-03-08 00:00"

ttdModel = TTD(time1, time2)
seat_times = ttdModel.get_seat_time()  # for most loader-methods
weektimes = ttdModel.get_weektimes()  # for comprehensible plots etc
weektimes = weektimes[...,np.newaxis]
print weektimes.shape
ttd = ttdModel.get_ttd()

# load deterministic timeofweek-variable using separate model
with open('../TTDWeek/model', 'r') as file:
    deterministic_model = cPickle.load(file)
det_times = deterministic_model.predict(weektimes)

# load movingaverage-variable vector using separate model
# TODO

# load vectors of state-variables at times weektimes()
t_waiters_loader = UntriagedLoader(time1, time2, 0)
t_waiters_loader.set_search_triage()
d_waiters_loader = UntriagedLoader(time1, time2, 0)
d_waiters_loader.set_search_doctor()
print t_waiters_loader

t_waiters = load_state_nbrs(seat_times, t_waiters_loader)
d_waiters = load_state_nbrs(seat_times, d_waiters_loader)
print t_waiters.shape, t_waiters
# TODO much more going herez

# save data
np.savez(
        'data.pkl',
        weektimes=weektimes,
        ttd=ttd,
        det_times=det_times,
        t_waiters=t_waiters,
        d_waiters=d_waiters
        )
