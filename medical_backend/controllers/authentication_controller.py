from flask_jwt_extended import create_access_token
from ..models import User, Patient, Appointments

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
        else:
            response, code = {"access_token": token, "role_id": uuser['role_id']}, 201
    return response, code