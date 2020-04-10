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

    if profile:
        response, code = {"profile": profile, "records": records, "prescriptions": rx, "appointments": appointments}, 200
    else:
        reponse, code = {"msg": "Bad patient id"}, 400

    return response, code

def get_patient_rx_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    rx = patient.get_patient_prescriptions(patient_id)

    if rx:
        response, code = rx, 200
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

def delete_appt_route(request):
    patient = Patient()
    appt_id = request.args.get("aid", None)
    answer = patient.delete_appointment(appt_id)
	
    if answer:
        response, code = {"msg": "Delete Successful"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400
    return response, code

