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
            occupied_rooms.append(hit["fields"]["Location"])


class room:
    def __init__(self, names, department):
        self.names = names
        self.department = department


class Rooms:
    rooms = [
        room(["ivr", "iv", "vr", "bvr", "gvr", "g", "b"], "waiting"),

        room(["i1", "1", "in1", "if1", "gi1", "bi1"], "infection"),
        room(["i2", "2", "in2", "if2", "gi2", "bi2"], "infection"),
        room(["i3", "3", "in3", "if3", "gi3", "bi3"], "infection"),
        room(["i4", "4", "in4", "if4", "gi4", "bi4"], "infection"),

        room(["T5", "5"], "triage"),
        room(["T6", "6"], "triage"),
        room(["T7", "7"], "triage"),
        room(["T8", "8"], "triage"),
        room(["T9", "9"], "triage"),

        room(["g10", "10"], "yellow"),
        room(["g11", "11"], "yellow"),
        room(["g12", "12"], "yellow"),
        room(["g13", "13"], "yellow"),
        room(["g14", "14"], "yellow"),
        room(["g15", "15"], "yellow"),
        room(["g16", "16"], "yellow"),
        room(["g17", "17"], "yellow"),
        room(["g18", "18"], "yellow"),

        room(["b19", "19"], "blue"),
        room(["b20", "20"], "blue"),
        room(["b21", "21"], "blue"),
        room(["b22", "22"], "blue"),
        room(["b23", "23"], "blue"),
        room(["b24", "24"], "blue"),
        room(["b25", "25"], "blue"),
        room(["b26", "26"], "blue"),
        room(["b27", "27"], "blue"),

        room(["30"], "barn_gyn_onh"),
        room(["31"], "barn_gyn_onh"),
        room(["32"], "barn_gyn_onh"),
        room(["33"], "barn_gyn_onh"),
        room(["34"], "barn_gyn_onh"),
        room(["35"], "barn_gyn_onh"),
        room(["46"], "barn_gyn_onh"),


        room(["36"], "orthopedia"),
        room(["37"], "orthopedia"),
        room(["38"], "orthopedia"),
        room(["39"], "orthopedia"),
        room(["40"], "orthopedia"),
        room(["41"], "orthopedia"),
        room(["42"], "orthopedia"),
        room(["43"], "orthopedia"),
        room(["44"], "orthopedia"),
        room(["45"], "orthopedia"),
        room(["47a"], "orthopedia"),
        room(["47b"], "orthopedia"),
        room(["48a"], "orthopedia"),
        room(["48b"], "orthopedia"),

        room(["50", "k50"], "surgery"),
        room(["51", "k51"], "surgery"),
        room(["52", "k52"], "surgery"),
        room(["53", "k53"], "surgery"),
        room(["54", "k54"], "surgery"),
        room(["55", "k55"], "surgery"),
        room(["56", "k56"], "surgery"),
        room(["57", "k57"], "surgery"),
        room(["58", "k58"], "surgery"),
        room(["59", "k59"], "surgery"),
        room(["60", "k60"], "surgery"),
        room(["61", "k61"], "surgery"),
        room(["62", "k62"], "surgery"),
        room(["63", "k63"], "surgery"),

        room(["A1"], "ambulance"),
        room(["A2"], "ambulance"),
        room(["A3"], "ambulance"),
        room(["A4"], "ambulance")
    ]
