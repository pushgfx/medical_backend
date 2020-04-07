from flask_jwt_extended import create_access_token
from ..models import Patient, User

def registration_route(request):
	patient = Patient()
	user = User()
	req_email = request.json.get("email", None)
	if user.check_user(req_email):
		response, code = {"msg": "Email already exists!"}, 401
	else:
		patient_id = patient.add_patient(request)
		user_id = {"uid":patient_id,"role":2}
		token = create_access_token(user_id)
		response, code = {"access_token": token, "role_id": 2, "patient_id": patient_id}, 201
	return response, code