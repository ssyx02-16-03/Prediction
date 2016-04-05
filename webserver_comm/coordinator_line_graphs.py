import time
from elastic_api.TimeToEventLoader import TimeToEventLoader
from PatientsFlows import RealTimeWait

ONE_HOUR_MILLISECONDS = 60 * 60 * 1000


def run():
    now = int(time.time()) * 1000

    end_time = now
    start_time = now - ONE_HOUR_MILLISECONDS * 5
    loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)

    # set times by means of fulhack
    loader.end_time = end_time
    loader.start_time = start_time

    loader.set_search_triage()
    ttt = get_vectors(loader)

    loader.set_search_doctor()
    ttd = get_vectors(loader)

    loader.set_search_removed()
    ttk = get_vectors(loader)

    return {
        "ttt": jsonize(ttt),
        "ttd": jsonize(ttd),
        "ttk": jsonize(ttk)
    }


def get_vectors(loader):
    ans = RealTimeWait.run(loader)
    x_axis = ans[0]
    y_axis = ans[1]
    return {
        "x_axis": x_axis,
        "y_axis": y_axis
    }


def jsonize(v):
    x = v["x_axis"]
    y = v["y_axis"]

    x_json = []
    for val in x:
        x_json.append(val[0])
    y_json = []
    for val in y:
        y_json.append(val)

    json = {
        "x_axis": x_json,
        "y_axis": y_json
    }
    return json
