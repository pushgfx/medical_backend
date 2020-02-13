# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ..models import Client

def get_client_route(request):
	client = Client()
	#Get the uid from token
	client_id = get_jwt_identity()['uid']
	profile = client.get_client_dict(client_id)
	if profile:
		response, code = {"profile": profile}, 200
	else:
		reponse, code = {"msg":"Bad client id"}, 400

	return response, code