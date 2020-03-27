#Flask and Flask Extension Imports
from ..models import Office

def get_offices_route():
	office = Office()
	offices = office.get_all_offices()
	if offices:
		response, code = {"offices": offices}, 200
	else:
		reponse, code = {"msg":"Bad request"}, 400

	return response, code

def get_offices_by_doctor_route(request):
	office = Office()
	doctor_id = request.args.get("did", None)
	offices = office.get_offices_by_doctor(str(doctor_id))
	if offices:
		response, code = {"offices": offices}, 200
	else:
		response, code = {"msg": "Bad doctor id"}, 400
	return response, code
