from flask_jwt_extended import create_access_token
from ..models import Client, User

def registration_route(request):
	client = Client()
	user = User()
	req_email = request.json.get("email", None)
	if user.check_user(req_email):
		response, code = {"msg": "Email already exists!"}, 401
	else:
		uid = client.add_client(request)
		user_id = {"uid":uid,"role":2}
		response, code = {"access_token": create_access_token(user_id)}, 201
	return response, code