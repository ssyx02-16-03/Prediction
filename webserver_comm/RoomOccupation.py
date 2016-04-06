from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader


def run():
    """
    This function queries the database for all occupied rooms. A list is compiled of all existing rooms and their number
    of occupants; room_json. A list is also compiled for all occupied rooms that were not expected to exist;
    weird_rooms_json.
    :return: json containing all rooms and their number of occupants
    """
    loader = CurrentFieldsLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
    loader.set_fields(["Location"])
    raw = loader.load_value(0, 0)

    occupied_rooms = []
    for hit in raw["hits"]["hits"]:
        occupied_rooms.append(hit["fields"]["Location"][0])

    # traverse list of occupied rooms
    weird_rooms = []
    rooms = Rooms().rooms
    for occupied_room in occupied_rooms:
        found = False
        for room in rooms:
            for name in room.names:
                occupied_room_name = str(occupied_room).lower()
                if occupied_room_name == name:  # flatten to lower case because json extractor uppercase them
                    room.occupants += 1
                    room.patient_department = get_patient_department(occupied_room_name)
                    found = True  # set found to true because it is not a weird_room
                    break
        if not found:  # if occupied_room was nowhere in Rooms().rooms it is a weird_room
            weird_rooms.append(occupied_room)

    # create json file for weird rooms
    weird_rooms_json = []
    for room in weird_rooms:
        found = False
        for weird_room_json in weird_rooms_json:
            if room == weird_room_json["room"]:
                weird_room_json["occupants"] += 1
                found = True
                break

        if not found:
            weird_rooms_json.append({
                "room": room,
                "occupied": True,  # if someone is in the room, someone is in the room
                "department": "unknown",
                "patient_department": get_patient_department(room)
            })

    # create json file for occupied rooms
    room_occupation_status = {
        "rooms": make_room_occupation_status(rooms),
        "weird_rooms": weird_rooms_json
    }

    unnoccupied_room_json = make_unoccupied_rooms(rooms)

    return room_occupation_status, unnoccupied_room_json


def make_room_occupation_status(rooms):
    room_json = {
        "nowhere":          [],
        "waiting":          [],
        "infection":        [],
        "triage":           [],
        "medicineYellow":   [],
        "medicineBlue":     [],
        "jour":             [],
        "orthoped":         [],
        "ort_cast":         [],
        "surgery":          [],
        "acute":            []
    }

    for room in rooms:
        room_json[room.department].append({
            "room":                  room.names[0],
            "occupied":              room.occupants > 0,
            "patient_department":    room.patient_department
        })

    return room_json


def make_unoccupied_rooms(rooms):
    unoccupied_room_json = {
        "medicineBlue": [],
        "medicineYellow": [],
        "surgery": [],
        "orthoped": [],
        "jour": []
    }
    for room in rooms:
        if room.occupants == 0:
            try:
                unoccupied_room_json[room.department].append({
                    "room": room.names[0]
                })
            except KeyError:
                pass
    return unoccupied_room_json


def get_patient_department(name):
    if name == "":  # dodge the array out of bounds exception
        return "default"

    first_letter = name[0].lower()
    if first_letter == "b":
        return "medicineBlue"

    if first_letter == "g":
        return "medicineYellow"

    return "default"


class Room:
    """
    This object represents one room in the emergency room.
    :param names a list of all the names the room is known by. names[0] is supposed to match the name on the actual map.
    """
    def __init__(self, names, department):
        self.names = names
        self.department = department
        self.occupants = 0
        self.patient_department = "default"


class Rooms:
    """
    This is the hard coded list of rooms in the emergency room.
    """
    def __init__(self):
        self.rooms = [
            Room(["noRoom", ""], "nowhere"),

            Room(["ivr", "iv", "vr", "bvr", "gvr", "g", "b", "giv", "biv"], "waiting"),

            Room(["1", "i1", "in1", "if1", "gi1", "bi1"], "infection"),
            Room(["2", "i2", "in2", "if2", "gi2", "bi2"], "infection"),
            Room(["3", "i3", "in3", "if3", "gi3", "bi3"], "infection"),
            Room(["4", "i4", "in4", "if4", "gi4", "bi4"], "infection"),

            Room(["5", "T5"], "triage"),
            Room(["6", "T6"], "triage"),
            Room(["7", "T7"], "triage"),
            Room(["8", "T8"], "triage"),
            Room(["9", "T9"], "triage"),

            Room(["10", "g10"], "medicineYellow"),
            Room(["11", "g11"], "medicineYellow"),
            Room(["12", "g12"], "medicineYellow"),
            Room(["13", "g13"], "medicineYellow"),
            Room(["14", "g14"], "medicineYellow"),
            Room(["15", "g15"], "medicineYellow"),
            Room(["16", "g16"], "medicineYellow"),
            Room(["17", "g17"], "medicineYellow"),
            Room(["18", "g18"], "medicineYellow"),

            Room(["19", "b19"], "medicineBlue"),
            Room(["20", "b20"], "medicineBlue"),
            Room(["21", "b21"], "medicineBlue"),
            Room(["22", "b22"], "medicineBlue"),
            Room(["23", "b23"], "medicineBlue"),
            Room(["24", "b24"], "medicineBlue"),
            Room(["25", "b25"], "medicineBlue"),
            Room(["26", "b26"], "medicineBlue"),
            Room(["27", "b27"], "medicineBlue"),

            Room(["30"], "jour"),
            Room(["31"], "jour"),
            Room(["32"], "jour"),
            Room(["33"], "jour"),
            Room(["34"], "jour"),
            Room(["35"], "jour"),
            Room(["46"], "jour"),

            Room(["36"],  "orthoped"),
            Room(["37"],  "orthoped"),
            Room(["38"],  "orthoped"),
            Room(["39"],  "orthoped"),
            Room(["40"],  "orthoped"),
            Room(["41"],  "orthoped"),
            Room(["42"],  "orthoped"),
            Room(["43"],  "orthoped"),
            Room(["44"],  "orthoped"),
            Room(["45"],  "orthoped"),

            Room(["47"],  "ort_cast"),
            Room(["47a"], "ort_cast"),
            Room(["47b"], "ort_cast"),
            Room(["48"],  "ort_cast"),
            Room(["48a"], "ort_cast"),
            Room(["48b"], "ort_cast"),

            Room(["50", "k50"], "surgery"),
            Room(["51", "k51"], "surgery"),
            Room(["52", "k52"], "surgery"),
            Room(["53", "k53"], "surgery"),
            Room(["54", "k54"], "surgery"),
            Room(["55", "k55"], "surgery"),
            Room(["56", "k56"], "surgery"),
            Room(["57", "k57"], "surgery"),
            Room(["58", "k58"], "surgery"),
            Room(["59", "k59"], "surgery"),
            Room(["60", "k60"], "surgery"),
            Room(["61", "k61"], "surgery"),
            Room(["62", "k62"], "surgery"),
            Room(["63", "k63"], "surgery"),

            Room(["A1"], "acute"),
            Room(["A2"], "acute"),
            Room(["A3"], "acute"),
            Room(["A4"], "acute")
        ]

def get_proper_room_name(my_name):
    rooms = Rooms()
    for room in rooms.rooms:
        for room_name in room.names:
            if room_name.lower() == my_name.lower():
                return room.names[0]

    return my_name  # no match found; my_name is weird room