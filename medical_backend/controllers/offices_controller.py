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


def update_offices_by_admin_route(request):
	office = Office()
	payload = request.get_json()['payload']
	office_id = payload['oid']
	office_name = payload['oname']
	office_street = payload['address']
	office_city = payload['city']
	office_state = payload['state']
	office_zipcode = payload['zipcode']
	office_phone = payload['phone']
	answer = office.update_office(office_id,office_name,office_street,office_city,office_state,office_zipcode,office_phone)

	if answer:
		response, code = {"msg" : "Office Updated"}, 200
	else:
		response, code = {"msg": "Bad Request "}, 400

	return response, code

