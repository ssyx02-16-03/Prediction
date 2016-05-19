from elastic_api.OngoingsLoaderList import OngoingsLoaderList
import time
import elastic_api.parse_date as parse_date
import matplotlib.pyplot as plt
start_time = "2016-04-25 00:00"
end_time = "2016-05-02 00:00"
interval = 10

loader = OngoingsLoaderList(start_time, end_time, interval)

v = loader.load_vector()
blues = []
yellows = []
for response in v:
    blue = 0
    yellow = 0
    for patient in response:
        room = patient["_source"]["Location"]
        print room
        if room and room[0] == "B":
            blue += 1
        if room and room[0] == "G":
            yellow += 1

    blues.append(blue)
    yellows.append(yellow)

plt.plot(blues, c='blue', label='blue')
plt.plot(yellows, c='black', label='yellow')
plt.legend(loc = "best")
plt.title(start_time + " to " + end_time)
plt.show()

all_patient = OngoingsLoaderList()