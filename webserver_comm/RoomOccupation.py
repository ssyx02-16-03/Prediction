# coding=utf-8
from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader

null_rooms = ["noRoom", ""]
waiting_rooms =["ivr", "iv", "vr", "bvr", "gvr", "giv", "biv"]
ignored_rooms = null_rooms + waiting_rooms

def run():
    """
    This function queries the database for all occupied rooms. A list is compiled of all existing rooms and their number
    of occupants; room_json. A list is also compiled for all occupied rooms that were not expected to exist;
    weird_rooms_json.
    :return: json containing all rooms and their number of occupants
    """
    loader = CurrentFieldsLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
    loader.set_fields(["Location","Team"])
    raw = loader.load_value(0, 0)

    occupied_rooms = []
    weird_rooms = []
    for hit in raw["hits"]["hits"]:
        raw_room_number = hit["fields"]["Location"][0]
        team = hit["fields"]["Team"][0]
        raw_room_number = raw_room_number.encode('utf-8').upper()

        occ_room = Room("5",raw_room_number, team)
        occ_room.occupy()
        occ_room.set_patient_department()
        occupied_rooms.append(occ_room)

    all_rooms = Rooms().all_rooms
    while(occupied_rooms.length > 0):
        new_room = occupied_rooms.pop()
        if contains(ignored_rooms, new_room.name):
            weird_rooms.append(new_room)
        else:
            all_rooms.insert(new_room)

    # create json file for occupied rooms
    room_occupation_status = {
        "rooms": make_room_occupation_status(all_rooms),
        "weird_rooms": weird_rooms
    }

    unnoccupied_room_json = make_unoccupied_rooms(all_rooms)
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
            "room":                  room.nr
            "occupied":              room.occupants > 0,
            "patient_department":    room.patient_department,
            "team":                  room.team
        })
    return room_json

#room_table generation
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
                    "room": room.nr
                })
            except KeyError:
                pass
    return unoccupied_room_json


class Room:
    """
    This object represents one room in the emergency room.
    :param names a list of all the names the room is known by. names[0] is supposed to match the name on the actual map.
    """
    def __init__(self, nr,name, team):
        self.nr = nr
        self.team = team
        self.name = name

    def __init__(self, nr, nameArray, department):
        self.nr = nr
        self.department = department
        self.name
        self.occupants = 0
        self.team

    def occupy():
        self.occupants++

    def set_patient_department():
        name = self.name
        if name == "":  # dodge the array out of bounds exception
            return

        if isinstance(name, int):
            self.nr = name
            room.department = "default"
            return

        try:
            first_letter = name[0].lower()
        except:
            return

        if first_letter == "b" or first_letter == "B":
            room.department = "medicineBlue"
            return

        if first_letter == "g" or first_letter == "G":
            room.department =  "medicineYellow"
            return

        if first_letter == "k" or first_letter == "K":
            room.department =  "surgery"
            return

        if first_letter == "o" or first_letter == "O":
            room.department =  "orthoped"
            return

        if first_letter == "j" or first_letter == "J":
            room.department =  "jour"
            return

class Rooms:
    """
    This is the hard coded list of rooms in the emergency room.
    """
    def __init__(self):
        self.all_rooms = [
            Room("1",["1", "i1", "in1", "if1", "gi1", "bi1"], "infection"),
            Room("2",["2", "i2", "in2", "if2", "gi2", "bi2"], "infection"),
            Room("3",["3", "i3", "in3", "if3", "gi3", "bi3"], "infection"),
            Room("4",["4", "i4", "in4", "if4", "gi4", "bi4"], "infection"),

            Room("5",["5", "T5"], "triage"),
            Room("6",["6", "T6"], "triage"),
            Room("7",["7", "T7"], "triage"),
            Room("8",["8", "T8"], "triage"),
            Room("9",["9", "T9"], "triage"),

            Room("10",["10", "g10"], "medicineYellow"),
            Room("11",["11", "g11"], "medicineYellow"),
            Room("12",["12", "g12"], "medicineYellow"),
            Room("13",["13", "g13"], "medicineYellow"),
            Room("14",["14", "g14"], "medicineYellow"),
            Room("15",["15", "g15"], "medicineYellow"),
            Room("16",["16", "g16"], "medicineYellow"),
            Room("17",["17", "g17"], "medicineYellow"),
            Room("18",["18", "g18"], "medicineYellow"),

            Room("19",["19", "b19"], "medicineBlue"),
            Room("20",["20", "b20"], "medicineBlue"),
            Room("21",["21", "b21"], "medicineBlue"),
            Room("22",["22", "b22"], "medicineBlue"),
            Room("23",["23", "b23"], "medicineBlue"),
            Room("24",["24", "b24"], "medicineBlue"),
            Room("25",["25", "b25"], "medicineBlue"),
            Room("26",["26", "b26"], "medicineBlue"),
            Room("27",["27", "b27"], "medicineBlue"),

            Room("30",["30"], "jour"),
            Room("31",["31"], "jour"),
            Room("32",["32"], "jour"),
            Room("33",["33"], "jour"),
            Room("34",["34"], "jour"),
            Room("35",["35"], "jour"),
            Room("46",["46"], "jour"),

            Room("36",["36"],  "orthoped"),
            Room("37",["37"],  "orthoped"),
            Room("38",["38"],  "orthoped"),
            Room("39",["39"],  "orthoped"),
            Room("40",["40"],  "orthoped"),
            Room("41",["41"],  "orthoped"),
            Room("42",["42"],  "orthoped"),
            Room("43",["43"],  "orthoped"),
            Room("44",["44"],  "orthoped"),
            Room("45",["45"],  "orthoped"),

            Room("47",["47"],  "ort_cast"),
            Room("47a",["47a"], "ort_cast"),
            Room("47b",["47b"], "ort_cast"),
            Room("48",["48"],  "ort_cast"),
            Room("48a",["48a"], "ort_cast"),
            Room("48b",["48b"], "ort_cast"),

            Room("50",["50", "k50"], "surgery"),
            Room("51",["51", "k51"], "surgery"),
            Room("52",["52", "k52"], "surgery"),
            Room("53",["53", "k53"], "surgery"),
            Room("54",["54", "k54"], "surgery"),
            Room("55",["55", "k55"], "surgery"),
            Room("56",["56", "k56"], "surgery"),
            Room("57",["57", "k57"], "surgery"),
            Room("58",["58", "k58"], "surgery"),
            Room("59",["59", "k59"], "surgery"),
            Room("60",["60", "k60"], "surgery"),
            Room("61",["61", "k61"], "surgery"),
            Room("62",["62", "k62"], "surgery"),
            Room("63",["63", "k63"], "surgery"),

            Room("A1",["A1"], "acute"),
            Room("A2",["A2"], "acute"),
            Room("A3",["A3"], "acute"),
            Room("A4",["A4"], "acute")
        ]

    def insert(new_room):
        for room in self.all_rooms:
            if(room.nr == new_room.nr):
                new_room.department = room.department
                room = new_room
                return


def get_proper_room_name(my_name): //not used atm
    try:
        allRooms = Rooms()
        for room in rooms.rooms:
            for room_name in room.names:
                if room_name.encode('utf-8').lower() == my_name.encode('utf-8').lower():
                    return room.names[0]
    except UnicodeEncodeError:
        return "error"
    return my_name  # no match found; my_name is weird room


def contains(room_list, my_room):
    """
    checks if my_room is in room_list
    __contains__() did not work as intended for some reason
    """
    for room in room_list:
        if room.decode('utf-8').lower() == my_room.decode('utf-8').lower():
            return True
    return False
