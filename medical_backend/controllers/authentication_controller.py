from flask_jwt_extended import create_access_token
from ..models import User

def authenticate_route(request):
    user = User()
    req_username = request.form['username']
    req_password = request.form['password']

    uuser = user.check_user(req_username)

    if not user.check_user(req_username):
        response, code = {"msg": "Bad username or password"}, 401
    elif not user.check_password(req_username, req_password):
        response, code = {"msg": "Bad username or password"}, 401
    else:
        user = {"uid":uuser['user_role_id'],"role":uuser['role_id']}
        response, code = {"access_token": create_access_token(user)}, 201
    return response, code