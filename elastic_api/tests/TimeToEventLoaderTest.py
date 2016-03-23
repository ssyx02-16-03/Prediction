from elastic_api.TimeToEventLoader import TimeToEventLoader
import time
import elastic_api.parse_date as parse_date
start_time = "2016-03-21 14:00"
end_time = "2016-03-22 14:00"
interval = 60 *1000

turbo = TimeToEventLoader(end_time, end_time, interval)
time_point = parse_date.date_to_millis(start_time)

turbo.set_search_triage()
print turbo.load_value(time_point, 60*60*1000)
print turbo.load_vector()
