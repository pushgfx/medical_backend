# Standard Lib Imports
import re

# Flask and Flask Extension Imports
from flask_jwt_extended import create_access_token
from ..models import User

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

def registration_route(request):
    req_username = request.json.get("username", None)
    req_password = request.json.get("password", None)
    role_id = 1
    # This method needs to be built in the User model
    # user = User.query.filter_by(username=req_username).first()

    # FOR TESTING
    usern = getUser(req_username)
    passw = getUser(req_password)
    # FOR TESTING

    if usern:
        response, code = {"msg": "Username already exists!"}, 401
    else:
        User.add_user(req_username,req_password)
        # Insert the new user into users table, and clients or doctors table
        # Then create a token and return to user so that they are automatically logged in
        user_id = {"uid":1}
        response, code = {"access_token": create_access_token(user_id)}, 201
    return response, code