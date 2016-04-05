import sys

from elastic_api.GeneralQuery import GeneralQuery
import RoomOccupation
from webserver_comm import name_generator
from elastic_api import parse_date
import time
num_lines = 3


def run():
    medicine_patients = GeneralQuery().get_patients_of_team("NAKME")

    blue_patients = []
    yellow_patients = []

    # if location starts with "b"/"g", add them to blue/yellow department and remove them from medicine_patients
    for patient in medicine_patients:
        # put every patient into the correct side
        department = RoomOccupation.get_patient_department(patient["Location"])
        if department == "medicineBlue":
            blue_patients.append(patient)
        elif department == "medicineYellow":
            yellow_patients.append(patient)
        else:
            yellow_patients.append(patient)
            blue_patients.append(patient)

    blue_events = get_recent_events(blue_patients)
    yellow_events = get_recent_events(yellow_patients)

    blue_json = []
    yellow_json = []

    for event in blue_events:
        blue_json.append(event.get_line())
    for event in yellow_events:
        yellow_json.append(event.get_line())

    return {
        "blue": blue_json,
        "yellow": yellow_json
    }


def get_recent_events(patients):
    all_events = []
    for patient in patients:
        try:
            updates = patient["Updates"]
            for update in updates:
                all_events.append(GenericEvent(
                    cc_id=[update["CareContactId"], ""],
                    name=name_generator.get_name_as_array(update["CareContactId"]),
                    modification_field=[update["ModifiedField"], update["ModifiedFrom"] + " -> " + update["ModifiedTo"]],
                    millis_since=int(time.time()*1000 - parse_date.date_to_millis(update["Timestamp"])),
                    current_location=[patient["Location"], ""]
                ))
        except KeyError:
            pass

        events = patient["Events"]
        for event in events:
            all_events.append(GenericEvent(
                cc_id=event["CareEventId"],
                name=name_generator.get_name_as_array(event["CareEventId"]),
                modification_field=[event["Title"], event["Value"]],
                millis_since=int(time.time()*1000 - parse_date.date_to_millis(event["Start"])),
                current_location=[patient["Location"], ""]
            ))

    return sort_by_time(all_events)[0:5]


def sort_by_time(events):
    new_list = []
    while events:
        latest = latest_event(events)
        new_list.append(latest)
        events.remove(latest)
    return new_list


def latest_event(events):
    old_time = sys.maxint
    current_best = -1
    for event in events:
        new_time = event.millis_since
        if new_time < old_time:
            current_best = event
            old_time = new_time
    return current_best


class GenericEvent:
    def __init__(self, cc_id, name, modification_field, millis_since, current_location):
        self.id = cc_id
        self.name = name
        self.modification_field = modification_field
        self.millis_since = millis_since
        self.current_location = current_location

    def get_line(self):
        return {
            "patient_id": self.id,
            "patient_name": self.name,
            "modification_field": self.modification_field,
            "minutes_since": [self.millis_since / 1000 / 60, ""],
            "current_location": self.current_location
        }
