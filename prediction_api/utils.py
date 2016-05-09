import time
from datetime import datetime


def crapformat1_to_emills(date_time):
    """
    :param date_time: format "2016-03-07T03:52:00Z"
    :return: epoch_millis
    """
    es = long(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")))
    emills = es * 1000
    return emills


def crapformat2_to_emills(date_time):
    """
    :param date_time: format "2016-03-07 03:52"
    :return: epoch_millis
    """
    es = long(time.mktime(time.strptime(date_time, "%Y-%m-%d %H:%M")))
    emills = es * 1000
    return emills


def mins_to_emills(minutes):
    return minutes * 60 * 1000


def hrs_to_emills(hours):
    return hours * 60 * 60 * 1000


def weekday(emills):
    """
    :return: 0 for monday, 6 for sunday
    """
    day_string = datetime.fromtimestamp(emills / 1000).strftime("%A")
    day_int_map = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
        }
    return int(day_int_map[day_string])


def time_of_day(emills):
    """
    :return: milliseconds of course, cause they are awesome things.
    """
    hour = datetime.fromtimestamp(emills / 1000).strftime("%H")
    millisecond = hour * 60 * 60 * 1000
    return millisecond
