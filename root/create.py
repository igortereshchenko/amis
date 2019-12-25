from root.db import Database
from root.entities import Base, Doctor, Patient, Symptom, Contraindication, Drug

db = Database()
Base.metadata.create_all(db.engine)

# patient1 = Patient(username='helthyone', name='Bob',surname='Merlyn',birthdate='1998-06-22',sex='male',patient_password='asdasdzxczxcqweqwe123')
# patient2 = Patient(username='mestapesta', name='Karl',surname='Noster',birthdate='1997-12-03',sex='male',patient_password='Passwordqwerty')
# patient3 = Patient(username='greenhorse', name='Klaudia',surname='Lobster',birthdate='1996-09-12',sex='female',patient_password='myStrongPassword')
#
#
# with db:
#     db.createPatient(patient1)
#     db.createPatient(patient2)
#     db.createPatient(patient3)

#
# doctor1 = Doctor(doctor_username='mr.Help', name='Andrea', surname='Krentson', doctor_password='my_password12')
# doctor2 = Doctor(doctor_username='Alboa', name='Brend', surname='Strokla', doctor_password='superdoctor2')
# doctor3 = Doctor(doctor_username='ASFqefx', name='Valley', surname='Kuper', doctor_password='alohacaloha')
#
# with db:
#     db.createDoctor(doctor1)
#     db.createDoctor(doctor2)
#     db.createDoctor(doctor3)
#
# symptom1 = Symptom(symptom_name='Temperature')
# symptom2 = Symptom(symptom_name='Headache')
# symptom3 = Symptom(symptom_name='Stomachache')
#
# with db:
#     db.createSymptom(symptom1)
#     db.createSymptom(symptom2)
#     db.createSymptom(symptom3)
#
# contraindication1 = Contraindication(name='Allergy',
#                                      additional_info='The only contraindication applicable to all vaccines is a history of a severe allergic reaction after a prior dose of vaccine or to a vaccine constituent. Precautions are not contraindications, but are events or conditions to be considered in determining if the benefits of the vaccine outweigh the risks. Precautions stated in product labelling can sometimes be inappropriately used as absolute contraindications, resulting in missed opportunities to vaccinate.')
# contraindication2 = Contraindication(name='Pregnancy',
#                                      additional_info='Before a diagnosis of some conditions, your doctor may consider whether getting pregnant is safe for you or on the contrary it would aggravate the symptoms associated. In some cases, a pregnancy can turn out to be a life-threatening event for the woman and the baby, especially if you suffer from any of the following conditions:')
# contraindication3 = Contraindication(name='Drug Abuse',
#                                      additional_info='For more information you need contact to you doctor. Thank you.')
#
# with db:
#     db.createContradication(contraindication1)
#     db.createContradication(contraindication2)
#     db.createContradication(contraindication3)
#
# drug1 = Drug(drug_name='Aspirin', price=123, symptom_name='Headache', contraindication='Drug Abuse')
# drug2 = Drug(drug_name='Terafloo', price=144, symptom_name='Temperature', contraindication='Allergy')
# drug3 = Drug(drug_name='AntyStomach', price=96, symptom_name='Stomachache', contraindication='Pregnancy')
#
# with db:
#     db.createDrug(drug1)
#     db.createDrug(drug2)
#     db.createDrug(drug3)
