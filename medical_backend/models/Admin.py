from bcrypt import checkpw, gensalt, hashpw
from ..database import Database
from ..models import User

db = Database()

class Admin(User):
    def get_doctor_dict(self):
        sql = """SELECT doctors.first_name, doctors.middle_initial, doctors.last_name, doctors.phone,
        specializations.specialization_name
        FROM `doctors`, `specializations`
        WHERE doctors.specialist_id = specializations.specialist_id"""
        results = db.run_query(sql, ())
        doctors =[]
        for result in results:
            doctor = {
                "firstName": result['first_name'],
                "middleInit": result['middle_initial'],
                "lastName": result['last_name'],
                "phone": result['phone'],
                "specialization_name": result['specialization_name'],
                }
            doctors.append(doctor)
        return doctors

    def get_patient_dict(self):
        sql = "SELECT * FROM `patients`"
        results = db.run_query(sql, ())
        patients =[]
        for result in results:
            patient = {
                "firstName": result['first_name'],
                "middleInit": result['middle_initial'],
                "lastName": result['last_name'],
                "street": result['street_1'],
                "city": result['city'],
                "state": result['state'],
                "zipcode": result['zipcode'],
                "phone": result['phone'],
                "dob": result['date_of_birth'],
                "gender": result['gender'],
                "marital": result['marital_status'],
                "race": result['race'],
                "email": result['email'],
                "primary_doctor": result['primary_doctor']
                }
            patients.append(patient)
        return patients

    def get_appointment_dict(self):
        sql = """SELECT
            	appointments.appt_id,
            	CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
            	CONCAT(doctors.first_name," ",doctors.middle_initial, " ", doctors.last_name) AS doctor,
            	offices.office_name AS office,
            	appointments.was_referred, appointments.referring_doctor_id, appointments.appt_start_time, appointments.estimated_end_time,
            	appointments.appt_status, appointments.booking_date, appointments.booking_method, appointments.reason_for_visit
            FROM `appointments`, `doctors`,`offices`,`patients`
            WHERE appointments.patient_id = patients.patient_id AND
            	appointments.doctor_id = doctors.doctor_id AND
            	appointments.office_id = offices.office_id"""
        results = db.run_query(sql, params)
        appointments =[]
        for result in results:
            appointment = {
                "patient": result['patient'],
                "doctor": result['doctor'],
                "office": result['office'],
                "was_referred": result['was_referred'],
                "referring_doctor_id": result['referring_doctor_id'],
                "appt_start_time": result['appt_start_time'],
                "estimated_end_time": result['estimated_end_time'],
                "appt_status": result['appt_status'],
                "booking_date": result['booking_date'],
                "booking_method": result['booking_method'],
                "reason_for_visit": result['reason_for_visit']
                }
            appointments.append(appointment)
        return appointments

    def get_office_dict(self):
        sql = "SELECT * FROM `offices`"
        results = db.run_query(sql, params)
        offices =[]
        for result in results:
            office = {
                "office_name": result['office_name'],
                "street_1": result['street_1'],
                "city": result['city'],
                "state": result['state'],
                "zipcode": result['zipcode'],
                "phone": result['phone']
                }
            offices.append(office)
        return offices
