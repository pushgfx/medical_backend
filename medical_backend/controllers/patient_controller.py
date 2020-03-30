# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ..models import Patient


def get_patient_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    profile = patient.get_patient_dict(patient_id)
    """
    appointments = patient.get_patient_appt_hist(patient_id)
    prescriptions = patient.get_patient_prescriptions(patient_id)
    medical_records = patient.get_patient_medical_records(patient_id)"""
    if profile:
        response, code = {"profile": profile}, 200
    else:
        response, code = {"msg": "Bad patient id"}, 400

    return response, code

def get_patient_rx_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    rx = patient.get_patient_prescriptions(patient_id)

    if rx:
        response, code = rx, 200
    else:
        response, code = {"msg": "Bad patient id"}, 400

    return response, code 

def get_patient_records_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    print("GET INTO PATIENT RECORD PID= "+str(patient_id))
    records = patient.get_patient_records(patient_id)
    if records:
        response, code = records, 200
    else:
        response, code = {"msg": "Bad patient id"}, 400
    print(response)
    return response, code