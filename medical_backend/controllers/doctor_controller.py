# Flask and Flask Extension Imports
# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ..models import Doctor

def get_doctor_dates(request):
	doctor = Doctor()
	#Get the uid from token
	doctor_id = request.args.get("doctor_id", None)
	dates = doctor.get_dates_dict(doctor_id)
	if dates:
		response, code = {"dates": dates}, 200
	else:
		reponse, code = {"msg":"Bad doctor id"}, 400

	return response, code

def get_doctor_route(request):
	doctor = Doctor()
	doctor_id = get_jwt_identity()['uid']
	profile = doctor.get_doctor_dict(doctor_id)
	if profile:
		response, code = {"profile":profile}
	else: 
		reponse, code = {"msg": "Bad doctor id"}, 400

	return reponse, code