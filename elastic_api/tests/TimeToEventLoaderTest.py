from elastic_api.TimeToEventLoader import TimeToEventLoader
import time
start_time = "2016-03-10 14:00"
end_time = "2016-03-14 16:00"
interval = 60

turbo = TimeToEventLoader(start_time, end_time, interval)
time_point = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M"))) * 1000

turbo.set_search_triage()
print turbo.load_value(time_point, 60)
print turbo.load_vector()

#turbo.set_search_doctor()
#print turbo.load_value(start_time, 60)

#turbo.set_search_removed()
#print turbo.load_value(start_time, 60)

