# Flask and Flask Extension Imports
from ..models import Doctor
from flask_jwt_extended import get_jwt_claims, get_jwt_identity

def get_doctor_dates(request):
	doctor = Doctor()
	#Get the uid from token
	doctor_id = request.args.get("did", None)
	office_id = request.args.get("oid", None)
	dates = doctor.get_dates_dict(str(office_id), str(doctor_id))
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
		response, code = {"msg": "Error retreiving doctors"}
	return response, code

def get_doctors_by_office_route(request):
	doctor = Doctor()
	office_id = request.args.get("oid", None)
	doctors = doctor.get_doctors_by_office(office_id)
	print(doctors)
	if doctors:
		response, code = {"doctors": doctors}, 200
	else:
		response, code = {"msg": "Error retreiving doctors"}, 400
	return response, code

def get_doctor_route():
	doctor = Doctor()
	doctor_id = get_jwt_identity()['uid']
	profile = doctor.get_doctor_dict(doctor_id)
	doctor_patient = doctor.get_doctor_patient(doctor_id)
	patient_appointments = doctor.get_doctor_all_appointment(doctor_id)
	# TODO: I comment these 6 lines of code out, in case this is what you want to handle multiple requests
	# today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
	# future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
	# past_appointments=doctor.get_past_appts_by_doctor(doctor_id)
	if profile:
		response, code = {"doctors": profile, "patients": doctor_patient, "appointments": patient_appointments}, 200
		# response, code = {"doctors": profile, "patients": doctor_patient, "appointments": patient_appointments,
		# 					"todayAppointments":today_appointments,"futureAppointments":future_appointments,
		# 				  	"pastAppointments":past_appointments}, 200
	else:
		response, code = {"msg": "Bad doctor id"}, 400
	# print(response)

	return response, code

def get_doctor_appointments_route():
	doctor = Doctor()
	doctor_id = get_jwt_identity()['uid']
	patient_appointments = doctor.get_doctor_all_appointment(doctor_id)
	today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
	future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
	past_appointments=doctor.get_past_appts_by_doctor(doctor_id)
	if patient_appointments or today_appointments or future_appointments or past_appointments:
		response, code = {"appointments": patient_appointments,
							"todayAppointments":today_appointments,"futureAppointments":future_appointments,
						  	"pastAppointments":past_appointments}, 200
	else:
		response, code = {"msg": "Error retrieving appointment by doctor"}, 400
	print(response)

	return response, code