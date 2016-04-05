from elastic_api.GeneralQuery import GeneralQuery
import RoomOccupation

num_lines = 3

def run():
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
            yellow_patients.append(patient)
            blue_patients.append(patient)

    blue_events = get_recent_events(blue_patients)
    yellow_events = get_recent_events(yellow_patients)


def get_recent_events(patients):
    events = []
    for patient in patients:
        updates =
