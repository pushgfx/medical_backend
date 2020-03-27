from flask_jwt_extended import create_access_token
from ..models import User

def authenticate_route(request):
    user = User()
    req_email = request.json.get("email", None)
    req_password = request.json.get("password", None)

    uuser = user.check_user(req_email)

    if not uuser:
        response, code = {"msg": "Bad email"}, 401
    elif not user.check_password(req_email, req_password):
        response, code = {"msg": "Bad password"}, 401
    else:
        user = {"uid":uuser['user_role_id'],"role":uuser['role_id']}
        response, code = {"access_token": create_access_token(user), "role_id": uuser['role_id']}, 201
    return response, code