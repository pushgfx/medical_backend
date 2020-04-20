# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ..models import Patient, Appointments

def get_patient_route(request):
    patient = Patient()
    patient_id = request.args.get('pid', None)
    profile = patient.get_patient_dict(str(patient_id))
    records = patient.get_patient_records(str(patient_id))
    rx = patient.get_patient_prescriptions(str(patient_id))
    appointment = Appointments()
    appointments = appointment.get_patient_appt_hist(patient_id)
    messages=patient.get_patient_messages(str(patient_id))
    if profile:
        response, code = {"profile": profile, "records": records, "prescriptions": rx, "appointments": appointments,"messages":messages}, 200
    else:
        reponse, code = {"msg": "Bad patient id"}, 400
    return response, code

def get_patient_rx_route(request):
    patient = Patient()
    # Get the uid from token
    role_id = get_jwt_identity()['role']
    print(role_id)
    if role_id is 2:
        patient_id = get_jwt_identity()['uid']
    else:
        patient_id = request.args.get('patient_id', None)
    rx = patient.get_patient_prescriptions(patient_id)

    if rx:
        response, code = {"prescriptions": rx}, 200
    else:
        reponse, code = {"msg": "Bad patient id"}, 400

    return response, code

def get_patient_records_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    records = patient.get_patient_records(patient_id)
    if records:
        response, code = records, 200
    else:
        reponse, code = {"msg": "Bad patient id"}, 400
    return response, code

def update_patientprofile_route(request):
    patient = Patient()
    answer = patient.update_patient(request)

    if answer:
        response, code = {"msg" : "Patient Updated"}, 200
    else:
        response, code = {"msg": "Bad Request "}, 400

    return response, code
