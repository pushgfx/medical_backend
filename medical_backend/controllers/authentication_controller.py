import re
from flask_jwt_extended import create_access_token
from ..models import User

user = User()

def authenticate_route(request):
    req_username = request.form['username']
    req_password = request.form['password']

    if not user.check_user(req_username):
        response, code = {"msg": "Bad username or password"}, 401
    elif not user.check_password(req_username, req_password):
        response, code = {"msg": "Bad username or password"}, 401
    else:
        user_id = {"uid":1}
        response, code = {"access_token": create_access_token(user_id)}, 201
    return response, code