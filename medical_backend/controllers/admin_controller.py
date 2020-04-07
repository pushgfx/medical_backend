from ..models import Admin

def get_admin_route(request):
	admin = Admin()
	doctor_profiles= admin.get_doctor_dict()
	patient_profiles= admin.get_patient_dict()
	appointments = admin.get_appointment_dict()
	offices = admin.get_office_dict()
	if doctor_profiles and patient_profiles and appointments and offices:
		response, code = {"doctors": doctor_profiles,"patients" : patient_profiles, "apointments": appointments, "offices": offices}, 200
	else:
		reponse, code = {"msg":"Bad admini request"}, 400

	return response, code

