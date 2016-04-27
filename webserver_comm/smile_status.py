# coding=utf-8

from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
from PatientsFlows import RealTimeWait
import numpy as np
ONE_HOUR_MILLISECONDS = 60 * 60 * 1000
import time

doctor_stable_hysteresis = 5  # minutes per minute
doctor_normal_interval = {
    "good": 45,
    "bad": 120
}

done_stable_hysteresis = 10
done_normal_interval = {
    "good": 180,
    "bad": 360
}


def run(torg):

    x_plot = np.linspace(-120, 60, 100)
    now = int(time.time()) * 1000

    end_time = now + ONE_HOUR_MILLISECONDS
    start_time = now - ONE_HOUR_MILLISECONDS * 8

    matched_loader = TimeToEventConditionalLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
    matched_loader.end_time = end_time
    matched_loader.start_time = start_time


    matched_loader.set_teams(["NAKME"])
    matched_loader.set_torg("medicineBlue")

    matched_loader.set_search_removed()
    ttk = get_trend(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd = get_trend(matched_loader, x_plot)


    ttd_json = make_json(ttd, doctor_normal_interval)
    ttk_json = make_json(ttk, done_normal_interval)
    return ttd, ttk


def make_json(times, normal_interval):
    current_time = times[-1]["y"]
    if current_time > normal_interval["bad"]:
        mood = -1
    elif current_time < normal_interval["good"]:
        mood = 1
    else:
        mood = 0

    return {
        "value": int(current_time),
        "trend": 0,  # TODO
        "mood": mood
    }
