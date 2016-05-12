# -*- coding: utf-8 -*-
""" Module for loading "state"-like paramaters from Elasticsearch.

Methods in this module must take only one argument, timee, a time-variable in
epoch-millis, and return a number. If the returned number represents time, it
should also be in epoch-millis. Other kinds of methods do not belong here.
Private methods that take or return something else should me marked with _.
"""
from ESClient import ESClient
from elastic_api import parse_date
import shelve


class ClevererQuerier:
    """This Querier is a Clever one, he never sends the same query twice."""

    def __init__(self):
        # saves the dictionary on hard drive to not eat your RAM
        self.responses = shelve.open('tmpresponses')

    def _patients_in_window(self, time1, time2):
        query_id = str(time1) + str(time2)
        if query_id not in self.responses:
            client = ESClient()
            response = client.search(
                index="*",
                body={
                    "size": 10000,
                    "query": {
                        "match_all": {}
                    },
                    "filter": {
                        "and": [
                            {
                                "range": {
                                    "CareContactRegistrationTime": {
                                        "lte": time2,
                                        "format": "epoch_millis"
                                    }
                                }
                            },
                            {
                                "or": [
                                    {
                                        "match": {
                                            "_index": "on_going_patient_index"
                                        }
                                    },
                                    {
                                        "range": {
                                            "RemovedTime": {
                                                "gte": time1,
                                                "format": "epoch_millis"
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
            self.responses[query_id] = response["hits"]["hits"]
        return self.responses[query_id]

    def _events_in_window(self, time1, time2):
        patients_in_window = self._patients_in_window(time1, time2)
        events = []
        for patient in patients_in_window:
            for event in patient["_source"]["Events"]:
                event_time = parse_date.date_to_millis(event["Start"])
                if time1 < event_time < time2:
                    events.append(event)
        return events

    def _current_patients(self, timee):
        return self._patients_in_window(timee, timee)

    def _ttx_in_window(self, time1, time2, event_name):
        patients = self._patients_in_window(time1, time2)
        ttx_list = []
        for patient in patients:
            arrival_time = parse_date.date_to_millis(
                    patient["_source"]["CareContactRegistrationTime"])
            events = patient["_source"]["Events"]
            for event in events:
                if event["Title"] == event_name:
                    event_time = parse_date.date_to_millis(event["Start"])
                    if time1 < event_time < time2:
                        ttx_list.append(event_time - arrival_time)
        return ttx_list

    def _avg_ttx_in_window(self, time1, time2, event_name):
        ttx_list = self._ttx_in_window(time1, time2, event_name)
        if len(ttx_list) > 0:
            return int(sum(ttx_list) / len(ttx_list))
        else:
            return int(0)

    def _avg_future_ttx(self, timee, mins_fw, event_name):
        time_fw = timee + 1000 * 60 * mins_fw
        return self._avg_ttx_in_window(timee, time_fw, event_name)

    def _avg_rolling_ttx(self, timee, mins_bk, event_name):
        time_bk = timee - 1000 * 60 * mins_bk
        return self._avg_ttx_in_window(time_bk, timee, event_name)

    def avg_future_ttt_30(self, timee):
        return self._avg_future_ttx(timee, 30, "Triage")

    def avg_future_ttt_60(self, timee):
        """Return average ttt of triages occuring in future 60 minutes."""
        return self._avg_future_ttx(timee, 60, "Triage")

    def avg_future_ttt_120(self, timee):
        return self._avg_future_ttx(timee, 120, "Triage")

    def avg_future_ttk_30(self, timee):
        return self._avg_future_ttx(timee, 30, "Klar")

    def avg_future_ttk_60(self, timee):
        return self._avg_future_ttx(timee, 60, "Klar")

    def avg_future_ttk_120(self, timee):
        return self._avg_future_ttx(timee, 120, "Klar")

    def avg_rolling_ttk_30(self, timee):
        return self._avg_rolling_ttx(timee, 30, "Klar")

    def avg_rolling_ttk_60(self, timee):
        return self._avg_rolling_ttx(timee, 60, "Klar")

    def avg_rolling_ttk_120(self, timee):
        return self._avg_rolling_ttx(timee, 120, "Klar")

    def avg_rolling_ttt_30(self, timee):
        """Return average ttt of triages occuring in past 30 minutes."""
        return self._avg_rolling_ttx(timee, 30, "Triage")

    def avg_rolling_ttt_60(self, timee):
        """Return average ttt of triages occuring in past 60 minutes."""
        return self._avg_rolling_ttx(timee, 60, "Triage")

    def avg_rolling_ttt_120(self, timee):
        """Return average ttt of triages occuring in past 120 minutes."""
        return self._avg_rolling_ttx(timee, 120, "Triage")

    def avg_future_ttd_30(self, timee):
        return self._avg_future_ttx(timee, 30, u"Läkare")

    def avg_future_ttd_60(self, timee):
        """Return average ttd of triages occuring in future 60 minutes."""
        return self._avg_future_ttx(timee, 60, u"Läkare")

    def avg_future_ttd_120(self, timee):
        return self._avg_future_ttx(timee, 120, u"Läkare")

    def avg_rolling_ttd_30(self, timee):
        """Return average ttd of triages occuring in past 30 minutes."""
        return self._avg_rolling_ttx(timee, 30, u"Läkare")

    def avg_rolling_ttd_60(self, timee):
        """Return average ttd of triages occuring in past 60 minutes."""
        return self._avg_rolling_ttx(timee, 60, u"Läkare")

    def avg_rolling_ttd_120(self, timee):
        """Return average ttd of triages occuring in past 120 minutes."""
        return self._avg_rolling_ttx(timee, 120, u"Läkare")

    def _new_patients(self, timee, mins_bk):
        time_bk = timee - 1000 * 60 * mins_bk
        patients = self._current_patients(timee)
        count = 0
        for patient in patients:
            arrival_crap = patient["_source"]["CareContactRegistrationTime"]
            arrival_time = parse_date.date_to_millis(arrival_crap)
            if time_bk < arrival_time < timee:
                count += 1
        return count

    def new_patients_30(self, timee):
        return self._new_patients(timee, 30)

    def new_patients_60(self, timee):
        return self._new_patients(timee, 60)

    def new_patients_120(self, timee):
        return self._new_patients(timee, 120)

    def ongoings(self, timee):
        """Return total number of patients present at timee."""
        patients = self._current_patients(timee)
        return len(patients)

    def _ongoings_color(self, timee, color):
        patients = self._current_patients(timee)
        patients_color = self._color_sort(patients, color)
        return len(patients_color)

    def ongoings_blue(self, timee):
        return self._ongoings_color(timee, u"Blå")

    def ongoings_green(self, timee):
        return self._ongoings_color(timee, u"Grön")

    def ongoings_yellow(self, timee):
        return self._ongoings_color(timee, u"Gul")

    def ongoings_orange(self, timee):
        return self._ongoings_color(timee, u"Orange")

    def ongoings_red(self, timee):
        return self._ongoings_color(timee, u"Röd")

    def _unfinished(self, timee):
        patients = self._current_patients(timee)
        unfinished = []
        for patient in patients:
            events = patient["_source"]["Events"]
            for event in events:
                if event["Title"] == "Klar":
                    event_time = parse_date.date_to_millis(event["Start"])
                    if event_time > timee:
                        unfinished.append(patient)
        return unfinished

    def unfinished(self, timee):
        unfinished = self._unfinished(timee)
        return len(unfinished)

    def avg_wait_finished(self, timee):
        unfinisheds = self._unfinished(timee)
        waited_times = []
        for patient in unfinisheds:
                arr_crap = patient["_source"]["CareContactRegistrationTime"]
                arrival_time = parse_date.date_to_millis(arr_crap)
                waited_time = timee - arrival_time
                waited_times.append(waited_time)
        if len(waited_times) > 0:
            return int(sum(waited_times) / len(waited_times))
        else:
            return int(0)

    def _waiters(self, timee, event_name):
        patients = self._current_patients(timee)
        waiters = []
        for patient in patients:
            try:
                time_to_event = patient["_source"][event_name]
            except KeyError:
                time_to_event = -1
            reg_time_crap = patient["_source"]["CareContactRegistrationTime"]
            reg_time = parse_date.date_to_millis(reg_time_crap)
            event_time = reg_time + time_to_event
            if timee < event_time:
                waiters.append(patient)
        return waiters

    def _avg_wait_event(self, timee, event_name):
        waiters = self._waiters(timee, event_name)
        waited_time = []
        for waiter in waiters:
            arrival_crap = waiter["_source"]["CareContactRegistrationTime"]
            wait = timee - parse_date.date_to_millis(arrival_crap)
            waited_time.append(wait)
        if len(waited_time) > 0:
            return int(sum(waited_time) / len(waited_time))
        else:
            return int(0)

    def avg_wait_triage(self, timee):
        """Return average time waited of triage waiters."""
        return self._avg_wait_event(timee, "TimeToTriage")

    def avg_wait_doctor(self, timee):
        """Return average time waited of doctor waiters."""
        return self._avg_wait_event(timee, "TimeToDoctor")

    def _waiters_triage(self, timee):
        return self._waiters(timee, "TimeToTriage")

    def _waiters_doctor(self, timee):
        return self._waiters(timee, "TimeToDoctor")

    def untriageds(self, timee):
        """Return number of present but untriaged patients."""
        waiters = self._waiters_triage(timee)
        return len(waiters)

    def untreateds(self, timee):
        """Return number of present patients who haven't seen a doctor."""
        waiters = self._waiters_doctor(timee)
        return len(waiters)

    def _room_less_patients(self, timee):
        patients = self._current_patients(timee)
        room_less_patients = []
        for patient in patients:
            loc_string = patient["_source"]["Location"]
            if not any(char.isdigit() for char in loc_string):
                room_less_patients.append(patient)
        return room_less_patients

    def unroomed(self, timee):
        """Return present patients without an int in location field."""
        room_less_patients = self._room_less_patients(timee)
        return len(room_less_patients)

    def _unroomed_color(self, timee, color):
        patients = self._room_less_patients(timee)
        patients_color = self._color_sort(patients, color)
        return len(patients_color)

    def unroomed_blue(self, timee):
        return self._unroomed_color(timee, u"Blå")

    def unroomed_green(self, timee):
        return self._unroomed_color(timee, u"Grön")

    def unroomed_yellow(self, timee):
        return self._unroomed_color(timee, u"Gul")

    def unroomed_orange(self, timee):
        return self._unroomed_color(timee, u"Orange")

    def unroomed_red(self, timee):
        return self._unroomed_color(timee, u"Röd")

    def _ttt_zero_patients(self, timee):
        patients = self._current_patients(timee)
        ttt_zero_patients = []
        for patient in patients:
            if patient["_source"]["TimeToTriage"] == 0:
                ttt_zero_patients.append(patient)
        return ttt_zero_patients

    def larm_patients(self, timee):
        """Return present patients with ttt set to 0."""
        patients = self._ttt_zero_patients(timee)
        return len(patients)

    def larm_patients_untreated(self, timee):
        """Return untreated patients with ttt set to 0."""
        patients = self._ttt_zero_patients(timee)
        untreated = []
        for patient in patients:
            for event in patient["_source"]["Events"]:
                event_time_crap = event["Start"]
                event_time = parse_date.date_to_millis(event_time_crap)
                if event["Type"] == u"LÄKARE" and timee < event_time:
                    untreated.append(patient)
        return len(untreated)

    def _color_sort(self, patients, color):
        patients_color = []
        for patient in patients:
            if patient["_source"]["Priority"] == unicode(color):
                patients_color.append(patient)
        return patients_color

    def _waiters_doctor_color(self, timee, color):
        waiters = self._waiters_doctor(timee)
        waiters_color = self._color_sort(waiters, color)
        return waiters_color

    def untreateds_blue(self, timee):
        """Return number of present patients who haven't seen a doctor and has
        been given priority green.
        """
        untreadeds = self._waiters_doctor_color(timee, u"Blå")
        return len(untreadeds)

    def untreateds_green(self, timee):
        """Return number of present patients who haven't seen a doctor and has
        been given priority green.
        """
        untreadeds = self._waiters_doctor_color(timee, u"Grön")
        return len(untreadeds)

    def untreateds_yellow(self, timee):
        """Return number of present patients who haven't seen a doctor and has
        been given priority yellow.
        """
        untreadeds = self._waiters_doctor_color(timee, u"Gul")
        return len(untreadeds)

    def untreateds_orange(self, timee):
        """Return number of present patients who haven't seen a doctor and has
        been given priority orange.
        """
        untreadeds = self._waiters_doctor_color(timee, u"Orange")
        return len(untreadeds)

    def untreateds_red(self, timee):
        """Return number of present patients who haven't seen a doctor and has
        been given priority red.
        """
        untreadeds = self._waiters_doctor_color(timee, u"Röd")
        return len(untreadeds)

    def _type_events_in_window(self, time1, time2, typee):
        events_in_window = self._events_in_window(time1, time2)
        typee_events = []
        for event in events_in_window:
            if event["Type"] == unicode(typee):
                typee_events.append(event)
        return typee_events

    def _doctor_events_in_window(self, time1, time2):
        events_in_window = self._type_events_in_window(time1, time2, u"LÄKARE")
        return events_in_window

    def _triage_events_in_window(self, time1, time2):
        events_in_window = self._type_events_in_window(time1, time2, u"TRIAGE")
        return events_in_window

    def doctors(self, timee):
        """Return number of doctor tags in past hour events."""
        one_hr_bk = timee - 60 * 60 * 1000
        doctor_events = self._doctor_events_in_window(one_hr_bk, timee)
        doctor_tags = []
        for event in doctor_events:
            doctor_tags.append(event["Value"])
        unique_doctor_tags = set(doctor_tags)
        return len(unique_doctor_tags)

    def teams(self, timee):
        """Return number of team tags in past hour patients."""
        one_hr_bk = timee - 60 * 60 * 1000
        patients = self._patients_in_window(one_hr_bk, timee)
        team_tags = []
        for patient in patients:
            team_tags.append(patient["_source"]["Team"])
        unique_team_tags = set(team_tags)
        return len(unique_team_tags)

    def speed_doctors_30(self, timee):
        """Return number of doctor events in past 30 minutes."""
        half_hour_bk = timee - 30 * 60 * 1000
        doctor_events = self._doctor_events_in_window(half_hour_bk, timee)
        return len(doctor_events)

    def speed_doctors_60(self, timee):
        """Return number of doctor events in past 60 minutes."""
        one_hr_bk = timee - 60 * 60 * 1000
        doctor_events = self._doctor_events_in_window(one_hr_bk, timee)
        return len(doctor_events)

    def speed_doctors_120(self, timee):
        two_hr_bk = timee - 120 * 60 * 1000
        doctor_events = self._doctor_events_in_window(two_hr_bk, timee)
        return len(doctor_events)

    def speed_triage_30(self, timee):
        """Return number of triage events in past 30 minutes."""
        half_hr_bk = timee - 30 * 60 * 1000
        triage_events = self._triage_events_in_window(half_hr_bk, timee)
        return len(triage_events)

    def speed_triage_60(self, timee):
        """Return number of triage events in past 60 minutes."""
        one_hr_bk = timee - 60 * 60 * 1000
        triage_events = self._triage_events_in_window(one_hr_bk, timee)
        return len(triage_events)

    def speed_triage_120(self, timee):
        two_hr_bk = timee - 120 * 60 * 1000
        triage_events = self._triage_events_in_window(two_hr_bk, timee)
        return len(triage_events)

'''
# test
time1_crap = "2016-03-11 11:30"
time2_crap = "2016-03-11 19:00"
time1 = parse_date.date_to_millis(time1_crap)
time2 = parse_date.date_to_millis(time2_crap)

time_now_crap = "2016-03-11 14:54"
time_now = parse_date.date_to_millis(time_now_crap)
print time_now

cq = ClevererQuerier()

times = [time1, time2, time_now]
ongs = [cq.ongoings(time) for time in times]
unts = [cq.untriageds(time) for time in times]
drs = [cq.doctors(time) for time in times]
spdrs30 = [cq.speed_doctors_30(time) for time in times]
spdrs60 = [cq.speed_doctors_60(time) for time in times]
sptri30 = [cq.speed_triage_30(time) for time in times]
sptri60 = [cq.speed_triage_60(time) for time in times]
wtrsdr = [cq.untreateds(time) for time in times]
utrtdsblu = [cq.untreateds_blue(time) for time in times]
utrtdsgre = [cq.untreateds_green(time) for time in times]
utrtdsyel = [cq.untreateds_yellow(time) for time in times]
utrtdsora = [cq.untreateds_orange(time) for time in times]
utrtdsred = [cq.untreateds_red(time) for time in times]
unroomedz = [cq.unroomed(time) for time in times]
larms = [cq.larm_patients(time) for time in times]
teams = [cq.teams(time) for time in times]
fttt = [cq.avg_future_ttt_60(time) for time in times]
rttt60 = [cq.avg_rolling_ttt_60(time) for time in times]
rttt30 = [cq.avg_rolling_ttt_30(time) for time in times]
newp60 = [cq.new_patients_60(time) for time in times]
avgwtri = [cq.avg_wait_triage(time) for time in times]
avgwdoc = [cq.avg_wait_doctor(time) for time in times]
lpuntr = [cq.larm_patients_untreated(time) for time in times]
untrdsyel = [cq.untreateds_yellow(time) for time in times]
ongyel = [cq.ongoings_yellow(time) for time in times]
unryel = [cq.unroomed_yellow(time) for time in times]
rttd30 = [cq.avg_rolling_ttd_30(time) for time in times]
fttd60 = [cq.avg_future_ttd_60(time) for time in times]
fttk30 = [cq.avg_future_ttk_30(time) for time in times]
rttk30 = [cq.avg_rolling_ttk_60(time) for time in times]
unfin = [cq.unfinished(time) for time in times]
avgtfin = [cq.avg_wait_finished(time) for time in times]
print ongs, unts, drs, spdrs30, spdrs60, sptri30, sptri60, wtrsdr, utrtdsblu
print utrtdsgre, utrtdsyel
print utrtdsora, utrtdsred, unroomedz, larms, teams
print fttt, rttt30, rttt60, newp60
print avgwtri, avgwdoc, lpuntr, untrdsyel, ongyel, unryel
print rttd30, fttd60, fttk30, rttk30, unfin, ongs, avgtfin
'''
