from elastic_api.TimeToEventLoader import TimeToEventLoader
import time
import elastic_api.parse_date as parse_date
start_time = "2015-08-12 14:00"
end_time = "2015-08-13 15:00"
interval = 60

turbo = TimeToEventLoader(start_time, end_time, interval)
time_point = parse_date.date_to_millis(start_time)

turbo.set_search_triage()
print turbo.load_value(time_point, 2*60*60*1000)
#print turbo.load_vector()

#turbo.set_search_doctor()
#print turbo.load_value(start_time, 60)

#turbo.set_search_removed()
#print turbo.load_value(start_time, 60)

