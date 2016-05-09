import numpy as np
from elastic_api import parse_date
from WaitTimesPerPatient.TTD import TTD
from prediction_api.ClevererQuerier import ClevererQuerier
import cPickle


def to_vector(times, loader_function):
    vector = np.array([])
    i = 0
    for timee in times:
        i += 1
        if i % 20 == 0:
            print i
        vector = np.append(vector, loader_function(int(timee)))
    return vector.reshape(-1, 1)

time1_crap = "2016-03-08 00:00"
time2_crap = "2016-05-03 00:00"
time1 = parse_date.date_to_millis(time1_crap)
time2 = parse_date.date_to_millis(time2_crap)
time_list = range(time1, time2, 1000 * 60 * 60)

seat_times = time_list

#ttdModel = TTD(time1, time2)
#seat_times = ttdModel.get_seat_time()  # for most loader-methods
#weektimes = ttdModel.get_weektimes()  # for comprehensible plots etc
#weektimes = weektimes[..., np.newaxis]
#ttd = ttdModel.get_ttd().reshape(-1, 1)

# load deterministic timeofweek-variable vector using separate model
# with open('../TTDWeek/model.pkl', 'r') as file:
#     deterministic_model = cPickle.load(file)
# det_times = deterministic_model.predict(weektimes)

# load state-variable vectors
cq = ClevererQuerier()

fttt60 = to_vector(seat_times, cq.avg_future_ttt_60)

time = {}
#time["det_times"] = det_times
time["rttt30"] = to_vector(seat_times, cq.avg_rolling_ttt_30)
time["rttt60"] = to_vector(seat_times, cq.avg_rolling_ttt_60)

workload = {}
workload["untriaged"] = to_vector(seat_times, cq.untriageds)
workload["untreated"] = to_vector(seat_times, cq.untreateds)
workload["untreated_red"] = to_vector(seat_times, cq.untreateds_red)
workload["untreated_yellow"] = to_vector(seat_times, cq.untreateds_yellow)
workload["alarm"] = to_vector(seat_times, cq.larm_patients)
workload["ongoing"] = to_vector(seat_times, cq.ongoings)
workload["unroomed"] = to_vector(seat_times, cq.unroomed)

capacity = {}
capacity["doctors"] = to_vector(seat_times, cq.doctors)
capacity["teams"] = to_vector(seat_times, cq.teams)
capacity["speed_doctors_30"] = to_vector(seat_times, cq.speed_doctors_30)
capacity["speed_doctors_60"] = to_vector(seat_times, cq.speed_doctors_60)
capacity["speed_triage_30"] = to_vector(seat_times, cq.speed_triage_30)
capacity["speed_triage_60"] = to_vector(seat_times, cq.speed_triage_60)

data = dict(
        fttt60=fttt60,
        time=time,
        workload=workload,
        capacity=capacity,
        )
with open("data", "w") as file:
    cPickle.dump(data, file)
