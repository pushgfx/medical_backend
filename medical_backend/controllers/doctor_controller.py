# Flask and Flask Extension Imports
from ..models import Doctor
from flask_jwt_extended import get_jwt_claims, get_jwt_identity

def get_doctor_dates(request):
	doctor = Doctor()
	#Get the uid from token
	doctor_id = request.args.get("doctor_id", None)
	dates = doctor.get_dates_dict(str(doctor_id))
	if dates:
		response, code = {"dates": dates}, 200
	else:
		reponse, code = {"msg":"Bad doctor id"}, 400

	return response, code

def get_all_doctors():
	doctor = Doctor()
	doctors = doctor.get_doctors()
	if doctors:
		response, code = {"doctors": doctors}, 200
	else:
		response, code = {"msg": "Error retreiving doctors"}
	return response, code

def get_doctor_route(doctor_id):

	doctor = Doctor()
	doctor_id = get_jwt_identity()['uid']
	profile = doctor.get_doctor_dict(doctor_id)
	doctor_patient = doctor.get_doctor_patient(doctor_id)
	patient_appointment = doctor.get_doctor_all_appointment(doctor_id)
	if profile:
		response, code = {"profile":profile, "patients":doctor_patient, "appointments today": patient_appointment}, 200
	else:
		response, code = {"msg": "Bad doctor id"}, 400

	return response, code
