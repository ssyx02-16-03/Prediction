# coding=utf-8
from elastic_api.GeneralQuery import GeneralQuery
import RoomOccupation
elastic = GeneralQuery()


def run():
    """
    This will return a json containing all the data needed by the bar graph on the coordinator view
    """

    medicine_patients = get_patients("NAKME")  # aquire all medicine patients
    medicine_patients_blue = []
    medicine_patients_yellow = []
    medicine_patients_nocolor = []
    # place patients into the right medicine side, based on the name of their location. If medicine side is ambiguous,
    # place them into medicine_patients_nocolor
    for patient in medicine_patients:
        print patient["Location"]
        color = RoomOccupation.get_patient_department(patient["Location"])
        if color == "medicineYellow":
            medicine_patients_yellow.append(patient)
        elif color == "medicineBlue":
            medicine_patients_blue.append(patient)
        else:
            medicine_patients_nocolor.append(patient)

    # surgery and orthoped patients are very straightforward
    surgery_patients = get_patients("NAKKI")
    orthoped_patients = get_patients("NAKOR")

    # onh/gyn/barn
    onh_gyn_barn_patients = get_patients(u"NAKÖN") + get_patients("NAKBA")

    # finally, find all patients that do not belong to any of NAKME, NAKKI, NAKOR, NAKÖN, NAKBA
    all_patients = get_all_patients()
    other_department_patients = get_other_department_patients(all_patients)

    return {
        "total_patients":             len(all_patients),
        "untriaged":                  get_untriaged(all_patients),
        "medicineBlue":               make_bars(medicine_patients_blue),
        "medicineYellow":             make_bars(medicine_patients_yellow),
        "medicineNoColor":            make_bars(medicine_patients_nocolor),
        "surgery":                    make_bars(surgery_patients),
        "orthoped":                   make_bars(orthoped_patients),
        "onhGynBarn":                 make_bars(onh_gyn_barn_patients),
        "otherDepartmentPatients":    make_bars(other_department_patients)
    }


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
    return n


def make_bars(patients):
    """
    Loops through a list of patients and counts priorities and doctor statuses. Also counts how many have been triaged.

    :param patients: list of patients
    :return: json containing all the data needed to generate the bar graph
    """

    data = BarGroup()  # create an empty bar graph dataset
    data.totalPatients = len(patients)

    for patient in patients:
        # count how many patients are on each priority level
        prio = patient["Priority"]
        has_priority = True
        if prio == u"Blå":
            data.blue += 1
        elif prio == u"Grön":
            data.green += 1
        elif prio == u"Gul":
            data.yellow += 1
        elif prio == u"Orange":
            data.orange += 1
        elif prio == u"Röd":
            data.red += 1
        else:
            data.no_prio += 1
            has_priority = False

        # check what the doctor status is
        if has_priority:  # if the patient has not been triaged, it has no doctor status
            is_klar = False
            for event in patient["Events"]:
                if event["Title"] == "Klar":
                    data.klar += 1
                    is_klar = True

            if not is_klar:  # if the patient is finished, it has no doctor status
                if patient["TimeToDoctor"] != -1:  #
                    data.has_doctor += 1

    return data.get_json()


class BarGroup:
    """
    This calss contains all the data needed to generate one section of the bar graph, both the priority and the doctor
    sides.
    """
    def __init__(self):
        self.totalPatients = 0
        self.klar = 0
        self.has_doctor = 0
        self.no_prio = 0
        self.blue = 0
        self.green = 0
        self.yellow = 0
        self.orange = 0
        self.red = 0
        self.incoming = 0  # how is this defined?

    def get_json(self):
        return {
            "klar": self.klar,
            "has_doctor": self.has_doctor,
            "no_doctor": self.totalPatients - self.has_doctor - self.klar - self.no_prio,
            "total_patients": self.totalPatients,

            "priority": {
                "blue": self.blue,
                "green": self.green,
                "yellow": self.yellow,
                "orange": self.orange,
                "red": self.red,
                "no_prio": self.no_prio
            }
        }


def get_patients(team):
    """
    Queries the database for all patients in the given team
    :param team: the team to search for
    :return: all patients currently under the given team, returned as an array
    """
    index = "on_going_patient_index"
    body = {
        "size": 10000,
        "query": {
            "match": {"Team": team}
        }
    }
    query = elastic.query(index=index, body=body)
    results = query["hits"]["hits"]
    patients = []
    for result in results:
        patients.append(result["_source"])
    return patients


def get_all_patients():
    """
    :return: array containg all patients currently at the emergency room.
    """
    index = "on_going_patient_index"
    body = {
        "size": 10000,
        "query": {
            "match_all": {}
        }
    }
    query = elastic.query(index=index, body=body)
    results = query["hits"]["hits"]
    patients = []
    for result in results:
        patients.append(result["_source"])
    return patients
