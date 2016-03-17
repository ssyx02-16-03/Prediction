import time
import AMQCommunication
from elastic_api.TimeToEventLoader import TimeToEventLoader

FRAME_TIME_INTERVAL = 0.5  # seconds
amq = AMQCommunication.Interface()
ONE_HOUR_MILLISECS = 60*60*1000

def main():
    """
    Calls iteration() with FRAME_TIME_INTERVAL intervals
    """
    while 1:
        last_time = time.time()
        iteration()
        if last_time + FRAME_TIME_INTERVAL - time.time() > 0:
            time.sleep(last_time + FRAME_TIME_INTERVAL - time.time())


def iteration():
    """
    One run of the loop.
    """
    data = time_to_event("Triage", 10, ONE_HOUR_MILLISECS)
    amq.send_package("triage_times_array", data)

    data = time_to_event("Doctor", 10, ONE_HOUR_MILLISECS)
    amq.send_package("doctor_times_array", data)

    data = time_to_event("Removed", 10, ONE_HOUR_MILLISECS)
    amq.send_package("removed_times_array", data)


def time_to_event(title, points, interval):
    """
    Calculates historic values for TTT, TTD or TTK. For each interval, calcuates the TTX for the patients that
    underwent event X during that interval.
    :param title: the event title to look for. Must be one of ["Triage", "Doctor, "Removed"]
    :param points: number of sample points
    :param interval: the time between sample points
    :return: a list containing the average time_to_event for each sample point
    """
    loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)  # constructor parameters are unused

    if title is "Triage":
        loader.set_search_triage()
    elif title is "Doctor":
        loader.set_search_doctor()
    elif title is "Removed":
        loader.set_search_removed()
    else:
        raise NameError

    times = []
    for n in range(1, points):
        times.append(loader.load_value(int(time.time() * 1000) - interval * n, interval))
    return times


if __name__ == '__main__':
    main()




