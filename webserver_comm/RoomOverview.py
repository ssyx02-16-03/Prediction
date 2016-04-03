# coding=utf-8
from elastic_api import parse_date
from elastic_api.GeneralQuery import GeneralQuery
import RoomOccupation
import time

blue_rooms = ["19", "20", "21", "22", "23", "24", "25", "26", "27",
              "b19", "b20", "b21", "b22", "b23", "b24", "b25", "b26", "b27"]

yellow_rooms = ["10", "11", "12", "13", "14", "15", "16", "17", "18",
                "g10", "g11", "g12", "g13", "g14", "g15", "g16", "g17", "g18"]

waiting_rooms = ["ivr", "iv", "vr", "bvr", "gvr", "g", "b", "giv", "biv"]

# these lists are used to generate fake names for the patients. CarecontactId is used as the seed
fake_first_names = ["qwert", "asdf", "namn", "bar", "foo"]
fake_last_names = ["aaaaaaa", "bbbbbb", "cccccc", "dddddd", "sdasdas", "sdfsaerpoaiu"]

# if time since last event is larger than this, "guideline_exceeded" will be True in the output json
guideline_time_limit_minutes = 75


def run():
    """
    This function will return a json with all the data needed to draw the patient overview for the blue and yellow
    medicine sides.
    """
    # collect all NAKME patients from the database
    medicine_patients = GeneralQuery().get_patients_of_team("NAKME")

    blue_patients = []
    yellow_patients = []
    sideless_patients = []  # patients that are neither blue nor yellow (medicine side wise, not priority)

    # if location starts with "b"/"g", add them to blue/yellow department and remove them from medicine_patients
    for patient in medicine_patients:
        # put every patient into the correct side
        department = RoomOccupation.get_patient_department(patient["Location"])
        if department == "medicineBlue":
            blue_patients.append(patient)
        elif department == "medicineYellow":
            yellow_patients.append(patient)
        else:
            sideless_patients.append(patient)

    # we now have one blue list, one yellow list and one list of non-blue, non-yellow medicine patients
    blue_side_json = []
    yellow_side_json = []

    # fill the jsons
    for patient in blue_patients:
        blue_side_json.append(make_patient_json(patient, "blue_side"))

    for patient in yellow_patients:
        yellow_side_json.append(make_patient_json(patient, "yellow_side"))

    for patient in sideless_patients:  # sideless patients end up in both the blue and yellow json
        patient_json = make_patient_json(patient, "no_side")
        blue_side_json.append(patient_json)
        yellow_side_json.append(patient_json)

    return {
        "blue": blue_side_json,
        "yellow": yellow_side_json
    }


def make_patient_json(patient, side):
    """
    This creates a json with the data to make one patient-rectangle on the patient overview

    :param patient: the patient object, directly from the database
    :param side: the value to put in the "side" field. will be one of "blue_side", "yellow_side" or "no_side"
    :return: one formatted patient object
    """
    doctor_name = get_doctor_name(patient["Events"])

    id = patient["CareContactId"]
    fake_name = fake_first_names[id % len(fake_first_names)] + " " + fake_last_names[id % len(fake_last_names)]

    last_event = get_last_event(patient["Events"])

    # parsing times
    parsed_time = time.strptime(patient["CareContactRegistrationTime"], u"%Y-%m-%dT%H:%M:%SZ")
    # adding some zeroes on manually. no preinvented wheel seemed to be readily availible so i reinvented it
    hour_of_day = str(parsed_time.tm_hour) if parsed_time.tm_hour >= 10 else "0" + str(parsed_time.tm_hour)
    minute_of_day  = str(parsed_time.tm_min) if parsed_time.tm_min >= 10 else "0" + str(parsed_time.tm_min)
    time_of_day = hour_of_day + ":" + minute_of_day

    return {
        "room": get_proper_room_name(patient["Location"]),
        "id": id,
        "side": side,
        "name": fake_name,
        "arrival_time_of_day": time_of_day,
        "last_event": {
            "minutes_since": last_event["minutes_since"],
            "name": last_event["name"],
            "guidelines_exceeded": last_event["guideline_exceeded"],
        },
        "has_doctor": doctor_name != "",  # if doctor has no name it does not exist
        "doctor_name": doctor_name,
        "Priority": patient["Priority"]
    }


def get_doctor_name(events):
    """
    loops through the event list to find the doctor assigend to the patient
    :param events: list of patient events, the "Event"-field
    :return: name of doctor, or empty strign if there is no doctor
    """
    name = ""
    for event in events:
        if event["Title"] == u"Läkare":
            name = event["Value"]
    return name


def get_last_event(events):
    """
    :param events: list of patient events, the "Event"-field
    :return: the latest event to happen in the list. If there is no event, it returns mostly empty fields.
    Note that "minutes_since" is a string
    """
    latest_time = 0
    name = ""
    for event in events:
        new_time = parse_date.date_to_millis(event["Start"])
        if new_time > latest_time:
            latest_time = new_time
            name = event["Title"]
    minutes_since = (time.time() - latest_time/1000) / 60
    if name == "":  # maybe this should instead default to arrival
        return {
            "name": "",
            "minutes_since": "",
            "guideline_exceeded": False
        }

    return {
        "name": name,
        "minutes_since": str(int(minutes_since)),
        "guideline_exceeded": minutes_since > guideline_time_limit_minutes
    }


def get_proper_room_name(name):
    """
    translates the name to a conventional one, for example "g10" -> "10" and "biv" -> "ivr"
    """
    return RoomOccupation.get_proper_room_name(name)


def contains(room_list, my_room):
    """
    checks if my_room is in room_list
    __contains__() did not work as intended for some reason
    """
    for room in room_list:
        if room.lower() == my_room.lower():
            return True
    return False


