import traceback

from root.db import Database


def get_doctors(db):
    doctors = []
    with db:
        db_doctors = db.fetchAllDoctors()
        for db_doctor in db_doctors:
            doctors.append({'doctor_username': db_doctor.doctor_username,
                            'doctor_password': db_doctor.doctor_password})
    return doctors


def get_patients(db):
    patients = []
    with db:
        db_patients = db.fetchAllPatients()
        for db_patient in db_patients:
            a = db_patient.username
            b = db_patient.patient_password
            patients.append({'username': a, 'patient_password': b})
    return patients


def unique_drug(drug):
    db = Database()
    with db:
        all_drugs = db.fetchAllDrugs()
        for db_drug in all_drugs:
            if db_drug.drug_name == drug:
                return False
    return True


def checkValues(drug, symptom, contra, price):
    if unique_drug(drug):
        try:
            float_price = float(price)
            if float_price <= 0:
                return "Price should be a positive number"
            return None
        except ValueError:
            traceback.print_exc()
            return "Price should be a positive number"
    return "This Drug already exists!"


def handle_extra_info(param):
    if param == '':
        return None
    return str(param)


def validate_doctor(username, name, surname, password, password1):
    db = Database()
    with db:
        doctor = db.fetchDoctor(username)
        if doctor:
            return "This username is occupied by other doctor. Please choose another"
        if password1 != password:
            return "Passwords don't match"
    return None


def validate_patient(username, name, surname, password, password1):
    db = Database()
    with db:
        patient = db.fetchDoctor(username)
        if patient:
            return "This username is occupied by other patient. Please choose another"
        if password1 != password:
            return "Passwords don't match"
    return None