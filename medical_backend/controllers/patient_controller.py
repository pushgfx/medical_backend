# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ..models import Patient


def get_patient_route(request):
    patient = Patient()
    # Get the uid from token
    patient_id = get_jwt_identity()['uid']
    profile = patient.get_patient_dict(patient_id)
    appointments = patient.get_patient_appt_hist(patient_id)
    prescriptions = patient.get_patient_prescriptions(patient_id)
    medical_records = patient.get_patient_medical_records(patient_id)
    if profile:
        response, code = {"profile": profile, "appointments": appointments,
            "prescriptions": prescriptions, "medical_records": medical_records}, 200
    else:
        reponse, code = {"msg": "Bad patient id"}, 400

    return response, code
