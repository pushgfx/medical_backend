# Standard Lib Imports
import re

# Flask and Flask Extension Imports
from flask_jwt_extended import create_access_token
from ..models import User

# User Defined Imports
# from fuelCost.database import db
# from fuelCost.models import User

user = User()

def getUser(uname):
    return user.get(arg)

def registration_route(request):
    if user.check_user(request.form['username']):
        response, code = {"msg": "Username already exists!"}, 401
    else:
        print("trying to add user")
        uid = user.add_client(request)
        user_id = {"uid":uid}
        response, code = {"access_token": create_access_token(user_id)}, 201
    return response, code