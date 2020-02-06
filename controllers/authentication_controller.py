# Standard Lib Imports
import re

# Flask and Flask Extension Imports
from flask_jwt_extended import create_access_token

# User Defined Imports
# from fuelCost.database import db
# from fuelCost.models import User

# FOR TESTING
user = {
    "username": "testuser",
    "password": "password"
}
# FOR TESTING

def getUser(uname):
    return user.get(arg)

def authenticate_route(request):
    req_username = request.json.get("username", None)
    req_password = request.json.get("password", None)

    # This method needs to be built in the User model
    # user = User.query.filter_by(username=req_username).first()

    # FOR TESTING
    usern = getUser(req_username)
    passw = getUser(req_password)
    # FOR TESTING

    if not usern:
        response, code = {"msg": "Bad username or password"}, 401
    elif not passw:
        response, code = {"msg": "Bad username or password"}, 401
    else:
        user_id = {"uid":uid}
        response, code = {"access_token": create_access_token(user_id)}, 201
    return response, code