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
                if str(occupied_room).lower() == name:  # flatten to lower case because json extractor uppercase them
                    room.occupants += 1
                    found = True  # set found to true because it is not a weird_room
                    break
        if not found:  # if occupied_room was nowhere in Rooms().rooms it is a weird_room
            weird_rooms.append(occupied_room)

    # create json file for weird rooms
    weird_rooms_json = []
    for room in weird_rooms:
        found = False
        for weird_room_json in weird_rooms_json:
            if room == weird_room_json["name"]:
                weird_room_json["occupants"] += 1
                found = True
                break

        if not found:
            weird_rooms_json.append({
                "room": room,
                "occupied": True  # if someone is in the room, someone is in the room
            })

    # create json file for rooms
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
            "room":         room.names[0],
            "occupied":    room.occupants > 0,
        })

    return {
        "rooms": room_json,
        "weird_rooms": weird_rooms_json
    }


class Room:
    """
    This object represents one room in the emergency room.
    :param names a list of all the names the room is known by. names[0] is supposed to match the name on the actual map.
    """
    def __init__(self, names, department):
        self.names = names
        self.department = department
        self.occupants = 0


class Rooms:
    """
    This is the hard coded list of rooms in the emergency room.
    """
    def __init__(self):
        self.rooms = [
            Room(["noRoom", ""], "nowhere"),

            Room(["ivr", "iv", "vr", "bvr", "gvr", "g", "b", "giv", "biv"], "waiting"),

            Room(["i1", "1", "in1", "if1", "gi1", "bi1"], "infection"),
            Room(["i2", "2", "in2", "if2", "gi2", "bi2"], "infection"),
            Room(["i3", "3", "in3", "if3", "gi3", "bi3"], "infection"),
            Room(["i4", "4", "in4", "if4", "gi4", "bi4"], "infection"),

            Room(["T5", "5"], "triage"),
            Room(["T6", "6"], "triage"),
            Room(["T7", "7"], "triage"),
            Room(["T8", "8"], "triage"),
            Room(["T9", "9"], "triage"),

            Room(["g10", "10"], "medicineYellow"),
            Room(["g11", "11"], "medicineYellow"),
            Room(["g12", "12"], "medicineYellow"),
            Room(["g13", "13"], "medicineYellow"),
            Room(["g14", "14"], "medicineYellow"),
            Room(["g15", "15"], "medicineYellow"),
            Room(["g16", "16"], "medicineYellow"),
            Room(["g17", "17"], "medicineYellow"),
            Room(["g18", "18"], "medicineYellow"),

            Room(["b19", "19"], "medicineBlue"),
            Room(["b20", "20"], "medicineBlue"),
            Room(["b21", "21"], "medicineBlue"),
            Room(["b22", "22"], "medicineBlue"),
            Room(["b23", "23"], "medicineBlue"),
            Room(["b24", "24"], "medicineBlue"),
            Room(["b25", "25"], "medicineBlue"),
            Room(["b26", "26"], "medicineBlue"),
            Room(["b27", "27"], "medicineBlue"),

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

            Room(["47"], "ort_cast"),
            Room(["47a"], "ort_cast"),
            Room(["47b"], "ort_cast"),
            Room(["48"], "ort_cast"),
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
