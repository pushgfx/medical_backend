from flask_jwt_extended import create_access_token
from ..models import Patient, User, Doctor

def registration_route(request):
	patient = Patient()
	user = User()
	req_email = request.json.get("email", None)
	if user.check_reg_user(req_email):
		response, code = {"msg": "Email already exists!"}, 401
	else:
		patient_id = patient.add_patient(request)
		user_id = {"uid":patient_id,"role":2}
		token = create_access_token(user_id)
		response, code = {"access_token": token, "role_id": 2, "patient_id": patient_id}, 201
	return response, code

def registration_doctor_route(request):
	doctor = Doctor()
	user = User()
	req_email = request.json.get("email", None)
	if user.check_reg_user(req_email):
		response, code = {"msg": "Email already exists!"}, 401
	else:
		doctor_id = doctor.add_doctor(request)
		user_id = {"uid":doctor_id,"role":3}
		response, code = {"doctorsList"}, 201
	return response, code 