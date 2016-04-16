# coding=utf-8
from elastic_api.GeneralQuery import GeneralQuery
import RoomOccupation
elastic = GeneralQuery()


blue_rooms = ["19", "20", "21", "22", "23", "24", "25", "26", "27",
              "b19", "b20", "b21", "b22", "b23", "b24", "b25", "b26", "b27"]

yellow_rooms = ["10", "11", "12", "13", "14", "15", "16", "17", "18",
                "g10", "g11", "g12", "g13", "g14", "g15", "g16", "g17", "g18"]

waiting_room_names = ["ivr", "iv", "vr", "bvr", "gvr", "g", "b", "giv", "biv"]


def run():
    """
    This will return a json containing all the data needed by the bar graph on the coordinator view
    """
    elastic = GeneralQuery()

    medicine_patients = elastic.get_patients_of_team("NAKME")  # aquire all medicine patients
    medicine_patients_blue = []
    medicine_patients_yellow = []
    medicine_patients_nocolor = []
    # place patients into the right medicine side, based on the name of their location. If medicine side is ambiguous,
    # place them into medicine_patients_nocolor
    for patient in medicine_patients:
        color = RoomOccupation.get_patient_department(patient["Location"])
        if color == "medicineYellow":
            medicine_patients_yellow.append(patient)
        elif color == "medicineBlue":
            medicine_patients_blue.append(patient)
        else:
            medicine_patients_nocolor.append(patient)

    # surgery and orthoped patients are very straightforward
    surgery_patients = elastic.get_patients_of_team("NAKKI")
    orthoped_patients = elastic.get_patients_of_team("NAKOR")

    # onh/gyn/barn
    onh_gyn_barn_patients = elastic.get_patients_of_team(u"NAKÖN") + elastic.get_patients_of_team("NAKBA")

    all_patients = elastic.get_all_patients()

    # with all patients aquired and sorted, start generating the data for the bar graphs
    # medicine_blue and medicine_yellow also need to sort out their room statuses
    medicine_blue = BarGroup(u"Medicin Blå")
    medicine_blue.make_bars(medicine_patients_blue)
    medicine_blue.make_room_status(medicine_patients_blue, blue_rooms)

    medicine_yellow = BarGroup("Medicin Gul")
    medicine_yellow.make_bars(medicine_patients_yellow)
    medicine_yellow.make_room_status(medicine_patients_yellow, yellow_rooms)

    medicine_nocolor = BarGroup("Medicin Övriga")
    medicine_nocolor.make_bars(medicine_patients_nocolor)

    surgery = BarGroup("Kirurg")
    surgery.make_bars(surgery_patients)

    orthoped = BarGroup("Ortoped")
    orthoped.make_bars(orthoped_patients)

    onhGynBarn = BarGroup("Jour")
    onhGynBarn.make_bars(onh_gyn_barn_patients)

    # all patients that do not belong to any of NAKME, NAKKI, NAKOR, NAKÖN, NAKBA
    other_department = BarGroup("Annan avdelning")
    other_department.make_bars(get_other_department_patients(all_patients))

    return {"bars":[
        get_untriaged(all_patients).get_json(),
        medicine_blue.get_json(),
        medicine_yellow.get_json(),
        medicine_nocolor.get_json(),
        surgery.get_json(),
        orthoped.get_json(),
        onhGynBarn.get_json(),
        other_department.get_json()
    ]}


def get_other_department_patients(patients):
    """
    :param patients: should be the list of all patients
    :return: every patient in the given list that are not handeld by any of the 5 main departments
    """
    other_patients = []
    for patient in patients:
        other = True
        for team in ["NAKME", "NAKKI", "NAKOR", u"NAKÖN", "NAKBA"]:
            if patient["Team"] == team:
                other = False
        if other:
            other_patients.append(patient)
    return other_patients


def get_untriaged(patients):
    """
    :param patients: list of patients
    :return: the number of patients in the list that have not received triage
    """
    n = 0
    for patient in patients:
        if patient["TimeToTriage"] == -1:
            n += 1

    bar = BarGroup("Inkommande")
    bar.untriaged = n
    return bar


class BarGroup:
    """
    This calss contains all the data needed to generate one section of the bar graph, both the priority and the doctor
    sides. Also room status where applicable
    """
    def __init__(self, division_name):
        # common data
        self.division_name = division_name
        self.totalPatients = 0
        self.incoming = 0

        self.untriaged = 0

        # doctor bar
        self.klar = 0
        self.has_doctor = 0

        # priority bar
        self.blue = 0
        self.green = 0
        self.yellow = 0
        self.orange = 0
        self.red = 0

        # room status bar
        self.has_rooms_status = False  # if this is false, get_json will not return any room data
        self.rooms_here = 0
        self.rooms_elsewhere = 0
        self.inner_waiting_room = 0
        self.at_examination = 0  # this is not well defined

    def make_bars(self, patients):
        """
        Loops through a list of patients and counts priorities and doctor statuses. Also counts how many have been triaged.

        :param patients: list of patients
        :return: json containing all the data needed to generate the bar graph
        """
        self.totalPatients = len(patients)

        for patient in patients:
            # count how many patients are on each priority level
            prio = patient["Priority"]
            has_priority = True
            if prio == u"Blå":
                self.blue += 1
            elif prio == u"Grön":
                self.green += 1
            elif prio == u"Gul":
                self.yellow += 1
            elif prio == u"Orange":
                self.orange += 1
            elif prio == u"Röd":
                self.red += 1
            else:
                self.incoming += 1
                has_priority = False

            # check what the doctor status is
            if has_priority:  # if the patient has not been triaged, it has no doctor status
                is_klar = False
                for event in patient["Events"]:
                    if event["Title"] == "Klar":
                        self.klar += 1
                        is_klar = True

                if not is_klar:  # if the patient is finished, it has no doctor status
                    if patient["TimeToDoctor"] != -1:  #
                        self.has_doctor += 1

    def get_json(self):
        if self.has_rooms_status:  # this will be the return for medicineBlue and medicineYellow
            return {
                "division": self.division_name,
                "total_patients": self.totalPatients,
                "incoming": self.incoming,

                "untriaged": self.untriaged,

                "blue": self.blue,
                "green": self.green,
                "yellow": self.yellow,
                "orange": self.orange,
                "red": self.red,

                "klar": self.klar,
                "has_doctor": self.has_doctor,
                "no_doctor": self.totalPatients - self.has_doctor - self.klar - self.incoming,

                "rooms_here": self.rooms_here,
                "rooms_elsewhere": self.rooms_elsewhere,
                "inner_waiting_room": self.inner_waiting_room,
                "at_examination": self.at_examination
            }
        else:  # this will be the return for all the other deparmtents
            return {
                "division": self.division_name,
                "total_patients": self.totalPatients,
                "incoming": self.incoming,

                "untriaged": self.untriaged,

                "blue": self.blue,
                "green": self.green,
                "yellow": self.yellow,
                "orange": self.orange,
                "red": self.red,

                "klar": self.klar,
                "has_doctor": self.has_doctor,
                "no_doctor": self.totalPatients - self.has_doctor - self.klar - self.incoming

            }

    def make_room_status(self, patients, local_rooms):
        """
        :param patients: lsit of patients in a deparment
        :param local_rooms: list of names of rooms in our department
        """
        self.has_rooms_status = True
        for patient in patients:
            room = patient["Location"].encode('utf-8').lower()
            if patient["Priority"] != "":
                # if list of waiting room names contains our room, patient is there
                if contains(waiting_room_names, room):
                    self.inner_waiting_room += 1

                # if input list of room names contains our room, patient is here
                elif contains(local_rooms, room):
                    self.rooms_here += 1

                # if neither list of room names contains our room, patient is somewhere
                else:
                    self.rooms_elsewhere += 1


def contains(room_list, my_room):
    """
    checks if my_room is in room_list
    __contains__() did not work as intended for some reason
    """
    for room in room_list:
        if room.lower() == my_room.lower():
            return True
    return False


