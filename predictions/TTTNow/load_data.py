from TTTNow.PresentTTT import PresentTTT

time1 = "2016-03-10 10:00"
time2 = "2016-03-10 11:00"

presentTTT = PresentTTT(time1, time2)
seat_time = presentTTT.get_seat_time()
ttt = presentTTT.get_ttt()

print int(seat_time[0]), ttt