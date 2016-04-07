# coding=utf-8
import time

from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
from PatientsFlows import RealTimeWait
import numpy as np
ONE_HOUR_MILLISECONDS = 60 * 60 * 1000

doctor_stable_hysteresis = 5  # minutes per minute
doctor_normal_interval = [45, 120]  # making up numbers as if i ran the place

done_stable_hysteresis = 10
done_normal_interval = [180, 360]


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
            "ttd": make_json(ttd_blue_med),
            "ttk": make_json(ttk_blue_med)
        },
        "yellow": {
            "ttd": make_json(ttd_yellow_med),
            "ttk": make_json(ttk_yellow_med)
        }
    }


def make_json(v):
    print v
    return 2


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
