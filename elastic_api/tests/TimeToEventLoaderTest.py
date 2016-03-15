from elastic_api.TimeToEventLoader import TimeToEventLoader
start_time = "2016-03-10 14:00"
end_time = "2016-03-14 00:00"
interval = 60

turbo = TimeToEventLoader(start_time, end_time, interval)

turbo.set_search_triage()
print turbo.load_value(start_time, 60)

turbo.set_search_doctor()
print turbo.load_value(start_time, 60)

turbo.set_search_removed()
print turbo.load_value(start_time, 60)

