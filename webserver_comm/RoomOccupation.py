from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader


class RoomOccupation:
    @staticmethod
    def run():
        """
        DON NOT USE: WORK IN PROGRESS
        :return:
        """
        loader = CurrentFieldsLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
        loader.set_fields(["Location"])
        raw = loader.load_value(0, 0)

        occupied_rooms = []
        for hit in raw["hits"]["hits"]:
            occupied_rooms.append(hit["fields"]["Location"][0])

        weird_rooms = []
        rooms = Rooms().rooms
        for occupied_room in occupied_rooms:
            found = False
            for room in rooms:
                for name in room.names:
                    if str(occupied_room).lower() == name:
                        room.occupants += 1
                        found = True
                        break
            if not found:
                weird_rooms.append(occupied_room)

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
                    "name": room,
                    "occupants": 1
                })

        room_json = []
        for room in rooms:
            room_json.append({
                "name": room.names[0],
                "occupants": room.occupants
            })

        return {
            "rooms": room_json,
            "weird_rooms": weird_rooms_json
        }



class Room:
    """
    This object represents one room in the emergency room.
    :param names a list of all the names the room is known by. This needs to be a list because there is no real
    names[0] is supposed to match the name on the actual map.
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

            Room(["g10", "10"], "yellow"),
            Room(["g11", "11"], "yellow"),
            Room(["g12", "12"], "yellow"),
            Room(["g13", "13"], "yellow"),
            Room(["g14", "14"], "yellow"),
            Room(["g15", "15"], "yellow"),
            Room(["g16", "16"], "yellow"),
            Room(["g17", "17"], "yellow"),
            Room(["g18", "18"], "yellow"),

            Room(["b19", "19"], "blue"),
            Room(["b20", "20"], "blue"),
            Room(["b21", "21"], "blue"),
            Room(["b22", "22"], "blue"),
            Room(["b23", "23"], "blue"),
            Room(["b24", "24"], "blue"),
            Room(["b25", "25"], "blue"),
            Room(["b26", "26"], "blue"),
            Room(["b27", "27"], "blue"),

            Room(["30"], "barn_gyn_onh"),
            Room(["31"], "barn_gyn_onh"),
            Room(["32"], "barn_gyn_onh"),
            Room(["33"], "barn_gyn_onh"),
            Room(["34"], "barn_gyn_onh"),
            Room(["35"], "barn_gyn_onh"),
            Room(["46"], "barn_gyn_onh"),

            Room(["36"],  "orthopedia"),
            Room(["37"],  "orthopedia"),
            Room(["38"],  "orthopedia"),
            Room(["39"],  "orthopedia"),
            Room(["40"],  "orthopedia"),
            Room(["41"],  "orthopedia"),
            Room(["42"],  "orthopedia"),
            Room(["43"],  "orthopedia"),
            Room(["44"],  "orthopedia"),
            Room(["45"],  "orthopedia"),
            Room(["47", "47a", "47b"], "orthopedia"),
            Room(["48", "48a", "48b"], "orthopedia"),

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

            Room(["A1"], "ambulance"),
            Room(["A2"], "ambulance"),
            Room(["A3"], "ambulance"),
            Room(["A4"], "ambulance")
        ]
