import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import root.credentials as credentials
from root.entities import Doctor, Symptom, Contraindication, Drug, Patient

from sqlalchemy import update


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    cstr = 'postgresql://{user}:{password}@{hostname}/{database}'.format(
        user=credentials.username,
        password=credentials.password,
        hostname=credentials.host,
        database=credentials.database
    )
    engine = db.create_engine(cstr)
    Session = sessionmaker(bind=engine)

    def __init__(self):
        # self.connection = self.engine.connect()
        self.session = None
        print("DB Instance created")

    def __enter__(self):
        if self.session is not None:
            self.session.close()
        self.session = self.Session()
        return self.session

    def __exit__(self, type, value, trace):
        if type is not None:
            print(f'Exeption happened in transaction:\n{value}')
            print(f'Trace:\n{trace}')
            self.session.rollback()
        else:
            print('transaction complete')
            self.session.commit()
        self.session.close()
        return True

    # Doctor

    def createDoctor(self, doctor):
        self.session.add(doctor)
        print("Doctor created successfully!")

    def updateDoctor(self, doctor_username, name, surname):
        dataToUpdate = {Doctor.name: name, Doctor.surname: surname}
        doctorData = self.session.query(Doctor).filter(Doctor.doctor_username == doctor_username)
        doctorData.update(dataToUpdate)
        print("Doctor updated successfully!")

    def fetchAllDoctors(self):
        doctors = self.session.query(Doctor).all()
        return doctors

    def fetchDoctor(self, doctor_username):
        doctor = self.session.query(Doctor).filter(Doctor.doctor_username == doctor_username).first()
        return doctor

    def deleteDoctor(self, doctor_username):
        doctorData = self.session.query(Doctor).filter(Doctor.doctor_username == doctor_username).first()
        self.session.delete(doctorData)
        print("Doctor deleted successfully!")

    # Patient
    def createPatient(self, patient):
        self.session.add(patient)
        print("Patient created successfully!")

    def updatePatient(self, username, name, surname, birthdate, sex):
        dataToUpdate = {Patient.name: name,
                        Patient.surname: surname, Patient.birthdate: birthdate,
                        Patient.sex: sex}
        patientData = self.session.query(Patient).filter(Patient.username == username)
        patientData.update(dataToUpdate)
        print("Patient updated successfully!")

    def fetchAllPatients(self):
        patients = self.session.query(Patient).all()
        return patients

    def fetchPatient(self, username):
        patient = self.session.query(Patient).filter(Patient.username == username).first()
        return patient

    def deletePatient(self, username):
        patientData = self.session.query(Patient).filter(Patient.username == username).first()
        self.session.delete(patientData)
        print("Patient deleted successfully!")

    # Symptom
    def createSymptom(self, symptom):
        self.session.add(symptom)
        print("Symptom created successfully!")

    def fetchAllSymptoms(self):
        symptoms = self.session.query(Symptom).all()
        return symptoms

    def fetchSymptom(self, symptom_name):
        symptom = self.session.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()
        return symptom

    def deleteSymptom(self, symptom_name):
        symptomData = self.session.query(Symptom).filter(Symptom.symptom_name == symptom_name).filter().first()
        self.session.delete(symptomData)
        print("Symptom deleted successfully!")

    def createDrug(self, drug):
        self.session.add(drug)
        print("Drug created successfully!")

    def fetchAllDrugs(self):
        drugs = self.session.query(Drug).all()
        return drugs

    def deleteDrug(self, drug_name):
        patientData = self.session.query(Drug).filter(Drug.drug_name == drug_name).first()
        self.session.delete(patientData)
        print("Drug deleted successfully!")

    def fetchDrugfromSymptom(self, symptom_name):
        drugs = self.session.query(Drug).filter(Drug.symptom_name == symptom_name).all()
        return drugs

    def updateDrug(self, drug_name, price):
        dataToUpdate = {Drug.price: price}
        drugData = self.session.query(Drug).filter(Drug.drug_name == drug_name)
        drugData.update(dataToUpdate)
        print("Drug updated successfully!")

    def close(self):
        self.session.close()

    def createContraindication(self, contradiction):
        self.session.add(contradiction)
        print("Contradiction created successfully!")

    def fetchAllContraindications(self):
        contras = self.session.query(Contraindication).all()
        return contras
