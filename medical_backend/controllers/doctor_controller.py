# Flask and Flask Extension Imports
from ..models import Doctor

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