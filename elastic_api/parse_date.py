import time


def date_to_millis(date):
    """
    Transforms a date to epoch-millis.

    Since the database uses three (or maybe four) different time formats and i did not want to fix that this function
    was needed. If you manage to crash this with a new date format, please append it to the list
    """
    formats = [u"%Y-%m-%dT%H:%M:%SZ", u"%Y-%m-%dT%H:%M:%S.000+0200", u"%Y-%m-%dT%H:%M:%S.000+0100", u"%Y-%m-%d %H:%M"]
    for format_string in formats:
        try:
            return long(time.mktime(time.strptime(date, format_string))) * 1000
        except ValueError:
            pass  # do nothing, try the next format in the list

    print "unrecognized format"
    raise ValueError


