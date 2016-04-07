# coding=utf-8
import time

from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
from PatientsFlows import RealTimeWait
import numpy as np
ONE_HOUR_MILLISECONDS = 60 * 60 * 1000


def run():

    x_plot = np.linspace(-120, 60, 100)
    now = int(time.time()) * 1000

    end_time = now + ONE_HOUR_MILLISECONDS
    start_time = now - ONE_HOUR_MILLISECONDS * 8

    loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
    # set times by means of fulhack
    loader.end_time = end_time
    loader.start_time = start_time

    loader.set_search_triage()
    ttt = get_vectors(loader, x_plot)

    loader.set_search_doctor()
    ttd = get_vectors(loader, x_plot)

    loader.set_search_removed()
    ttk = get_vectors(loader, x_plot)

    matched_loader = TimeToEventConditionalLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
    matched_loader.end_time = end_time
    matched_loader.start_time = start_time


    matched_loader.set_teams(["NAKME"])
    matched_loader.set_torg("medicineBlue")

    matched_loader.set_search_removed()
    ttk_blue_med = get_vectors(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_blue_med = get_vectors(matched_loader, x_plot)


    matched_loader.set_teams(["NAKME"])
    matched_loader.set_torg("medicineYellow")

    matched_loader.set_search_removed()
    ttk_yellow_med = get_vectors(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_yellow_med = get_vectors(matched_loader, x_plot)


    matched_loader.set_teams(["NAKKI"])
    matched_loader.set_torg("default")

    matched_loader.set_search_removed()
    ttk_surgery = get_vectors(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_surgery = get_vectors(matched_loader, x_plot)


    matched_loader.set_teams(["NAKOR"])
    matched_loader.set_torg("default")

    matched_loader.set_search_removed()
    ttk_ort = get_vectors(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_ort = get_vectors(matched_loader, x_plot)



    matched_loader.set_teams([u"NAKÖN", "NAKBA"])
    matched_loader.set_torg("default")

    matched_loader.set_search_removed()
    ttk_jour = get_vectors(matched_loader, x_plot)

    matched_loader.set_search_doctor()
    ttd_jour = get_vectors(matched_loader, x_plot)

    return {
        "ttt": jsonize_ttt(ttt),
        "ttd": jsonize_ttd_ttk(v=ttd, blue=ttd_blue_med, yellow=ttd_yellow_med,
                               surgery=ttd_surgery, orthopedia=ttd_ort, jour=ttd_jour),
        "ttk": jsonize_ttd_ttk(v=ttk, blue=ttk_blue_med, yellow=ttk_yellow_med,
                               surgery=ttk_surgery, orthopedia=ttk_ort, jour=ttk_jour)
    }


def get_vectors(loader, x_plot):
    start_index = 200
    ans = RealTimeWait.run(loader)
    y_axis = ans[1]

    trend = []
    prediction = []

    for i in range(0, 66):
        trend.append({
            "x": x_plot[i],
            "y": y_axis[i+start_index]
        })
    for i in range(66, 100):
        prediction.append({
            "x": x_plot[i],
            "y": y_axis[i+start_index]
        })

    return {
        "trend": trend,
        "prediction": prediction
    }


def jsonize_ttt(v):
    return {
        "trend": v["trend"],
        "prediction": v["prediction"]
    }


def jsonize_ttd_ttk(v, blue, yellow, surgery, orthopedia, jour):
    blue = (blue["prediction"][0])["y"]
    yellow = (yellow["prediction"][0])["y"]
    surgery = (surgery["prediction"][0])["y"]
    orthopedia = (orthopedia["prediction"][0])["y"]
    jour = (jour["prediction"][0])["y"]

    list = [blue, yellow, surgery, orthopedia, jour]
    list.sort()
    median = list[2]
    return {
        "trend": v["trend"],
        "prediction": v["prediction"],
        "times": {
            "Blue": blue,
            "Gul": yellow,
            "Ki": surgery,
            "Ort": orthopedia,
            "Jour": jour,
            "median": median
        }
    }
