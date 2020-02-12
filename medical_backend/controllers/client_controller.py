# Flask and Flask Extension Imports
from flask_jwt_extended import get_jwt_claims

def get_client_route(request):
	client = Client()
	#Get the uid from token
	client_id = get_jwt_claims()['user_role_id']
	profile = client.get_client(client_id)

	if profile:
		response, code = profile, 200
	else:
		reponse, code = {"msg":"Bad client id"}, 400

	return response, code