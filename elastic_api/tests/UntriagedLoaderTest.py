from elastic_api.UntriagedLoader import UntriagedLoader
import time
import elastic_api.parse_date as parse_date
start_time = "2016-03-17 21:00"
end_time = "2016-03-22 14:00"
interval = 30

turbo = UntriagedLoader(start_time, end_time, interval)
time_point = parse_date.date_to_millis(start_time)

print turbo.load_value(time_point, 60*60*1000)
print turbo.load_vector()
