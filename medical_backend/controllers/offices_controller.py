# Flask and Flask Extension Imports
from ..models import Offices

def get_offices_route(request):
	offices = Offices()
	offices = offices.get_offices()
	if offices:
		response, code = {"offices": offices}, 200
	else:
		reponse, code = {"msg":"Bad request"}, 400

	return response, code
