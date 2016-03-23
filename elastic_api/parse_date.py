import time
import calendar


def date_to_millis(date):
    """
    Transforms a date to epoch-millis.

    Since the database uses three (or maybe four) different time formats and i did not want to fix that, this function
    was needed. If you manage to crash this with a new date format, please append it to the list.

    Time zones are handled manually because it was convenient and i have no shame
    """

    ONE_HOUR_IN_SECONDS = 60 * 60
    try:
        return long(calendar.timegm(time.strptime(date, u"%Y-%m-%dT%H:%M:%SZ"))) * 1000
    except ValueError:
        try:
            return long(calendar.timegm(time.strptime(date, u"%Y-%m-%dT%H:%M:%S.000+0100")) - ONE_HOUR_IN_SECONDS) * 1000
        except ValueError:
            try:
                return long(calendar.timegm(time.strptime(date,  u"%Y-%m-%dT%H:%M:%S.000+0200")) - 2 * ONE_HOUR_IN_SECONDS) * 1000
            except ValueError:
                try:
                    return long(calendar.timegm(time.strptime(date, u"%Y-%m-%d %H:%M"))) * 1000
                except ValueError:
                    pass  # do nothing

    print "unrecognized date format: " + date
    raise ValueError
