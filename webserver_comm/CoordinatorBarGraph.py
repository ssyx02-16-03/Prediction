# coding=utf-8
from elastic_api.GeneralQuery import GeneralQuery
from elastic_api.CurrentFieldsLoader import CurrentFieldsLoader
import numpy
import time

import RoomOccupation
from elastic_api.UntriagedLoader import UntriagedLoader

elastic = GeneralQuery()



def run():
    """
    """

    medicine_patients = get_patients("NAKME")
    medicine_patients_blue = []
    medicine_patients_yellow = []
    medicine_patients_nocolor = []

    for patient in medicine_patients:
        color = RoomOccupation.get_patient_department(patient["Location"])
        if color == "medicineYellow":
            medicine_patients_yellow.append(patient)
        elif color == "medicineBlue":
            medicine_patients_blue.append(patient)
        else:
            medicine_patients_nocolor.append(patient)

    surgery_patients = get_patients("NAKKI")
    orthoped_patients = get_patients("NAKOR")
    onh_gyn_barn_patients = get_patients(u"NAKÖN") + get_patients("NAKBA")

    all_patients = get_all_patients()
    other_department_patients = get_other_department_patients(all_patients)

    return {
        "total_patients": len(all_patients),
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
    n = 0
    for patient in patients:
        if patient["TimeToTriage"] == -1:
            n += 1
    return n


def make_bars(patients):

    data = BarGroup()
    data.totalPatients = len(patients)

    for patient in patients:
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

        if has_priority:
            is_klar = False
            for event in patient["Events"]:
                if event["Title"] == "Klar":
                    data.klar += 1
                    is_klar = True

            if not is_klar:
                if patient["TimeToDoctor"] != -1:  #
                    data.has_doctor += 1

    return data.get_json()


class BarGroup:
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
