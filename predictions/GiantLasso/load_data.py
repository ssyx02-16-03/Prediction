import numpy as np
from elastic_api import parse_date
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

time1_crap = "2016-03-03 00:00"
time2_crap = "2016-05-02 00:00"
time1 = parse_date.date_to_millis(time1_crap)
time2 = parse_date.date_to_millis(time2_crap)
# 17 minute intervals to perhaps avoid some hourly patterns or something
times = np.array(range(time1, time2, 17 * 60 * 1000)).reshape(-1, 1)

cq = ClevererQuerier()

# this is stuff one might want to predict
future_time = {}
future_time["future_ttt30"] = to_vector(times, cq.avg_future_ttt_30)
future_time["future_ttt60"] = to_vector(times, cq.avg_future_ttt_60)
future_time["future_ttt120"] = to_vector(times, cq.avg_future_ttt_120)
future_time["future_ttd30"] = to_vector(times, cq.avg_future_ttd_30)
future_time["future_ttd60"] = to_vector(times, cq.avg_future_ttd_60)
future_time["future_ttd120"] = to_vector(times, cq.avg_future_ttd_120)

# these ones have the same dimension as the predicted variable
time = {}
time["rolling_ttt30"] = to_vector(times, cq.avg_rolling_ttt_30)
time["rolling_ttt60"] = to_vector(times, cq.avg_rolling_ttt_60)
time["rolling_ttt120"] = to_vector(times, cq.avg_rolling_ttt_120)
time["rolling_ttd30"] = to_vector(times, cq.avg_rolling_ttd_30)
time["rolling_ttd60"] = to_vector(times, cq.avg_rolling_ttd_60)
time["rolling_ttd120"] = to_vector(times, cq.avg_rolling_ttd_120)

# these ones probably have positive effect on wait time
workload = {}
workload["new30"] = to_vector(times, cq.new_patients_30)
workload["new60"] = to_vector(times, cq.new_patients_60)
workload["new120"] = to_vector(times, cq.new_patients_120)
workload["untriaged"] = to_vector(times, cq.untriageds)
workload["unroomed"] = to_vector(times, cq.unroomed)
workload["unroomed_blue"] = to_vector(times, cq.unroomed_blue)
workload["unroomed_green"] = to_vector(times, cq.unroomed_green)
workload["unroomed_yellow"] = to_vector(times, cq.unroomed_yellow)
workload["unroomed_orange"] = to_vector(times, cq.unroomed_orange)
workload["unroomed_red"] = to_vector(times, cq.unroomed_red)
workload["untreated"] = to_vector(times, cq.untreateds)
workload["untreated_blue"] = to_vector(times, cq.untreateds_blue)
workload["untreated_green"] = to_vector(times, cq.untreateds_green)
workload["untreated_yellow"] = to_vector(times, cq.untreateds_yellow)
workload["untreated_orange"] = to_vector(times, cq.untreateds_orange)
workload["untreated_red"] = to_vector(times, cq.untreateds_red)
workload["ongoing"] = to_vector(times, cq.ongoings)
workload["ongoing_blue"] = to_vector(times, cq.ongoings_blue)
workload["ongoing_green"] = to_vector(times, cq.ongoings_green)
workload["ongoing_yellow"] = to_vector(times, cq.ongoings_yellow)
workload["ongoing_orange"] = to_vector(times, cq.ongoings_orange)
workload["ongoing_red"] = to_vector(times, cq.ongoings_red)
workload["treated"] = workload["ongoing"] - workload["untreated"]
workload["treated_blue"] = workload["ongoing_blue"] -\
                            workload["untreated_blue"]
workload["treated_green"] = workload["ongoing_green"] -\
                            workload["untreated_green"]
workload["treated_yellow"] = workload["ongoing_yellow"] -\
                            workload["untreated_yellow"]
workload["treated_orange"] = workload["ongoing_orange"] -\
                            workload["untreated_orange"]
workload["treated_red"] = workload["ongoing_red"] - workload["untreated_red"]
workload["larm_untreated"] = to_vector(times, cq.larm_patients_untreated)
workload["larm"] = to_vector(times, cq.larm_patients)

# these ones probably have negative effect on wait time
capacity = {}
capacity["doctors"] = to_vector(times, cq.doctors)
capacity["teams"] = to_vector(times, cq.teams)
capacity["speed_doctors_30"] = to_vector(times, cq.speed_doctors_30)
capacity["speed_doctors_60"] = to_vector(times, cq.speed_doctors_60)
capacity["speed_doctors_120"] = to_vector(times, cq.speed_doctors_120)
capacity["speed_triage_30"] = to_vector(times, cq.speed_triage_30)
capacity["speed_triage_60"] = to_vector(times, cq.speed_triage_60)
capacity["speed_triage_120"] = to_vector(times, cq.speed_triage_120)

# no clue about the effect of these guys
unknown_dim = {}
unknown_dim["waited_triage"] = to_vector(times, cq.avg_wait_triage)
unknown_dim["waited_doctor"] = to_vector(times, cq.avg_wait_doctor)

data = dict(
        measurement_times=times,
        future_time=future_time,
        time=time,
        workload=workload,
        capacity=capacity,
        unknown_dim=unknown_dim,
        )
with open("data", "w") as file:
    cPickle.dump(data, file)
