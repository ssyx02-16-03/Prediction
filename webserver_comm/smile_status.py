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


def run():

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
    ttk_blue_med = get_trend(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_blue_med = get_trend(matched_loader, x_plot)


    matched_loader.set_teams(["NAKME"])
    matched_loader.set_torg("medicineYellow")

    matched_loader.set_search_removed()
    ttk_yellow_med = get_trend(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_yellow_med = get_trend(matched_loader, x_plot)

    return {
        "blue": {
            "ttd": make_json(ttd_blue_med, doctor_normal_interval, doctor_stable_hysteresis, 10),
            "ttk": make_json(ttk_blue_med, done_normal_interval, done_stable_hysteresis, 20)
        },
        "yellow": {
            "ttd": make_json(ttd_yellow_med, doctor_normal_interval, doctor_stable_hysteresis, 10),
            "ttk": make_json(ttk_yellow_med, done_normal_interval, done_stable_hysteresis, 20)
        }
    }


def make_json(times, normal_interval, hysteresis, lookback_samples):
    velocity = get_velocity(times[len(times)-lookback_samples: len(times)])
    if velocity > done_stable_hysteresis:
        trend = 1
    elif velocity < - done_stable_hysteresis:
        trend = -1
    else:
        trend = 0

    current_time = times[-1]["y"]
    if current_time > normal_interval["bad"]:
        mood = -1
    elif current_time < normal_interval["good"]:
        mood = 1
    else:
        mood = 0

    return {
        "value": int(current_time),
        "trend": trend,
        "mood": mood
    }


def get_trend(loader, x_plot):
    start_index = 200
    ans = RealTimeWait.run(loader)
    y_axis = ans[1]

    trend = []

    for i in range(0, 66):
        trend.append({
            "y": y_axis[i+start_index]
        })

    return trend


def get_velocity(times):
    time_differences = []
    first_time = times[0]["y"]
    for a_time in times:
        time_differences.append(a_time["y"] - first_time)

    # print time_differences

    weighted_differences = []
    for i in range(1, len(times)):
        weighted_differences.append(time_differences[i] / i)

   # print average(weighted_differences)
    return average(weighted_differences)


def average(vector):
    sum = 0
    for v in vector:
        sum += v
    return sum / len(vector)

