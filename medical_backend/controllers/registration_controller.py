from flask_jwt_extended import create_access_token
from ..models import Client

client = Client()

def registration_route(request):

    if client.check_user(request.json.get("email")):
        response, code = {"msg": "Email already exists!"}, 401
    else:
        uid = client.add_client(request)
        user_id = {"uid":uid}
        response, code = {"access_token": create_access_token(user_id)}, 201
    return response, code