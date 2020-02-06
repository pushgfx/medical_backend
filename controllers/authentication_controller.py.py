# Standard Lib Imports
import re

# Flask and Flask Extension Imports
from flask_jwt_extended import create_access_token

# User Defined Imports
from fuelCost.database import db
from fuelCost.models import User


def authenticate(request):
    req_username = request.json.get("username", None)
    req_password = request.json.get("password", None)

    user = User.query.filter_by(username=req_username).first()

    if not user:
        response, code = {"msg": "Bad username or password"}, 401
    elif not user.check_password(req_password):
        response, code = {"msg": "Bad username or password"}, 401
    else:
        response, code = {"access_token": create_access_token(user.user_id)}, 201
    return response, code


def register_user(request):
    req_username = request.json.get("username", None)
    req_email = request.json.get("email", None)
    req_password = request.json.get("password", None)

    if not req_username:
        response, code = {"message": "Invalid Username"}, 400

    elif User.query.filter_by(username=req_username).first():
        response, code = {"message": "Username already exists"}, 401

    elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", req_email):
        response, code = {"message": "Invalid Email"}, 400

    elif User.query.filter_by(email=req_email).first():
        response, code = {"message": "Email already exists"}, 401

    elif not req_password:
        response, code = {"message": "Invalid Password"}, 400

    else:
        user = User()
        user.username = req_username
        user.email = req_email
        user.set_password(req_password)
        db.session.add(user)

        # Creating Empty Profile for USER
        # This needs to be redone on both ends as this is bad form
        db.session.commit()
        response, code = {"access_token": create_access_token(user.user_id)}, 201

    return response, code
