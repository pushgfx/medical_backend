# Flask and Flask Extension Imports
from ..models import Doctor
from flask_jwt_extended import get_jwt_claims, get_jwt_identity

def get_doctor_dates(request):
    doctor = Doctor()
    #Get the uid from token
    doctor_id = request.args.get("did", None)
    office_id = request.args.get("oid", None)
    patient_id = get_jwt_identity()['uid']
    dates = doctor.get_dates_dict(str(office_id), str(doctor_id), str(patient_id))
    if dates:
        response, code = {"dates": dates}, 200
    else:
        reponse, code = {"msg": "Bad doctor id"}, 400
    return response, code

def get_all_doctors():
    doctor = Doctor()
    doctors = doctor.get_doctors()
    if doctors:
        response, code = {"doctors": doctors}, 200
    else:
        response, code = {"msg": "Error retreiving doctors"}, 400
    return response, code

def get_doctors_by_office_route(request):
    doctor = Doctor()
    office_id = request.args.get("oid", None)
    doctors = doctor.get_doctors_by_office(office_id)
    if doctors:
        response, code = {"doctors": doctors}, 200
    else:
        response, code = {"msg": "Error retreiving doctors"}, 400
    return response, code

def get_doctor_data_route():
    doctor = Doctor()
    doctor_id = get_jwt_identity()['uid']
    profile = doctor.get_doctor_dict(doctor_id)
    doctor_patient = doctor.get_doctor_patient(doctor_id)
    today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
    future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
    past_appointments=doctor.get_past_appts_by_doctor(doctor_id)
    medication_names=doctor.get_all_medications()
    medication_forms=doctor.get_all_medication_forms()
    approve_appointments = doctor.get_referred_appts_by_doctor(doctor_id);

    if profile:
        response, code = {"profile": profile, "patients": doctor_patient, "appointments":{"todayAppointments":today_appointments, "futureAppointments":future_appointments, "pastAppointments":past_appointments,"approveAppointments":approve_appointments},"medications":{"medicationNames":medication_names,"medicationForms":medication_forms}}, 200
    else:
        response, code = {"msg": "Bad doctor id"}, 400
    return response, code

def get_doctor_profile_route(request):
    doctor = Doctor()
    doctor_id = request.args.get('did')
    profile = doctor.get_doctor_dict(doctor_id)
    if profile:
        response, code = {"profile": profile} , 200
    else:
        response, code = {"msg": "Bad doctor id"}, 400

    return response, code

def get_doctor_appointments_route():
    doctor = Doctor()
    doctor_id = get_jwt_identity()['uid']
    today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
    future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
    past_appointments=doctor.get_past_appts_by_doctor(doctor_id)
    approve_appointments=doctor.get_referred_appts_by_doctor(doctor_id)

    if today_appointments or future_appointments or past_appointments:
        response, code = {"appointments":{"todayAppointments":today_appointments,"futureAppointments":future_appointments,
                            "pastAppointments":past_appointments,"approveAppointments":approve_appointments}}, 200
    else:
        response, code = {"msg": "Error retrieving appointment by doctor"}, 400
    # print(response)
    return response, code

def update_doctorprofile_route(request):
    doctor = Doctor()
    answer = doctor.update_doctor(request)

    if answer:
        response, code = {"msg" : "Doctor Updated"}, 200
    else:
        response, code = {"msg": "Bad Request "}, 400

    return response, code

def insert_new_prescription_route(request):
    doctor = Doctor()
    doctor_id = get_jwt_identity()['uid']
    new_prescription = doctor.add_patient_prescription(request, doctor_id)
    if new_prescription:
        response, code ={"addedPrescription": new_prescription}, 200
    return response, code

def get_all_specializations():
    doctor = Doctor()
    specializations = doctor.get_specializations()
    if specializations:
        response, code = {"specializations": specializations}, 200
    else:
        response, code = {"msg": "Error retreiving specializations"}, 400
    return response, code

def insert_new_record_route(request):
    doctor = Doctor()
    doctor_id = get_jwt_identity()['uid']
    new_record = doctor.add_patient_record(request, doctor_id)
    if new_record:
        response, code ={"record": new_record}, 200
    return response, code

def get_doctors_appointment(request):
    doctor = Doctor()
    patient_id = get_jwt_identity()['uid']
    doctors = doctor.get_appointment_doctor(patient_id)
    if doctors:
        response, code = {"doctors": doctors}, 200
    else:
        response, code = {"msg": "Error retreiving doctors"}, 400
    return response, code


def approve_specialist_appt_route(request):
    doctor = Doctor()
    answer = doctor.approve_specialist_appt(request)
    if answer:
        response, code = {"msg": "Appointment is Approved"}, 200
    else:
        response, code = {"msg": "Bad Request "}, 400
    return response, code

def get_all_physician(request):
    doctor = Doctor()
    physician = doctor.get_primary_physician()
    if physician:
        response, code = {"doctors": physician}, 200
    else:
        response, code = {"msg": "Error retreiving doctors"}, 400
    return response, code


def update_prescription(request):
    answer = Doctor().update_patient_prescription(request)
    return ({"msg" : "Prescription Updated"}, 200) if answer else ({"msg": "Bad Request "}, 400)

def get_medications():
    answer = Doctor().get_all_medications()
    return (answer, 200) if answer else ({"msg": "Bad Request "}, 400)

def get_dose_forms():
    answer = Doctor().get_all_dose_forms()
    return (answer, 200) if answer else ({"msg": "Bad Request "}, 400)

def update_record_route(request):
    answer = Doctor().update_record(request)
    return ({"msg" : "Record Updated"}, 200) if answer else ({"msg": "Bad Request "}, 400)
