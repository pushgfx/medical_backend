from flask_jwt_extended import create_access_token
from ..models import User, Patient, Appointments, Doctor

def authenticate_route(request):
    user = User()
    req_email = request.json.get("email", None)
    req_password = request.json.get("password", None)

    uuser = user.check_user(req_email)

    if not uuser:
        response, code = {"msg": "Bad email"}, 401
    elif not user.check_password(req_email, req_password):
        response, code = {"msg": "Bad password"}, 401
    else:
        user = {"uid":uuser['user_role_id'],"role":uuser['role_id']}
        token = create_access_token(user)
        if user['role'] == 2:
            patient = Patient()
            patient_id = user['uid']
            profile = patient.get_patient_dict(patient_id)
            records = patient.get_patient_records(patient_id)
            rx = patient.get_patient_prescriptions(patient_id)
            appointment = Appointments()
            appointments = appointment.get_patient_appt_hist(patient_id)
                # get all the data
            response, code = {"access_token": token, "role_id": uuser['role_id'], "profile": profile, "records": records, "prescriptions": rx, "appointments": appointments}, 201
        if user['role'] == 3:
            doctor = Doctor()
            doctor_id = user['uid']
            profile = doctor.get_doctor_dict(doctor_id)
            doctor_patient = doctor.get_doctor_patient(doctor_id)
            patient_appointments = doctor.get_doctor_all_appointment(doctor_id)
            today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
            future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
            past_appointments=doctor.get_past_appts_by_doctor(doctor_id)      
            response, code = {"access_token": token, "role_id": uuser['role_id'], "profile": profile, "patients": doctor_patient, "appointments":{"todayAppointments":today_appointments, "futureAppointments":future_appointments, "pastAppointments":past_appointments}}, 200      
        else:
            response, code = {"access_token": token, "role_id": uuser['role_id']}, 201
    return response, code