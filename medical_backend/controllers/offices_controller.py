#Flask and Flask Extension Imports
from ..models import Doctors

def get_offices_route(request):
	offices = Doctors()
	offices = offices.get_all_offices()
	if offices:
		response, code = {"offices": offices}, 200
	else:
		reponse, code = {"msg":"Bad request"}, 400

	return response, code
