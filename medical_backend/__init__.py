# Stadard Library Imports
import os

# Flask and Flask Extension Imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt_claims,
)

"""
    DO NOT IMPORT ANY USER DEFINED CODE HERE
    THAT RELIES ON THE APPLICATION STATE.

    YOU MAY HAVE CIRCULARE IMPORT ISSUES

    THIS INCLUDES:
        1. Controllers
"""

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # Checks Environmnet Variable And Builds from Config Object
        app.config.from_object(os.environ["APP_SETTINGS"])
        # Adding CORS to the App -- not neccesary in testing
        # May be wrong, but we can look into it later
        CORS(app)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Initializing Token Management
    jwt = JWTManager(app)

    """
        BEWARE!!!!!!!
        Controllers Are Defined Here To Avoid Circular Import
        Issues
    """
    from medical_backend.controllers import (
        authenticate_route,
        registration_route,
    )

    """
        Adding the User ID to the Token
        The ID Will Be Used for Queries
        We Need to Modify the Front End
        To Reflect Changes

    """

    @jwt.user_claims_loader
    def add_claims_to_access_token(id):
        return {"user_id": id}

    """
        THE FOLLOWING ROUTES ARE UNPROTECTED
        THEY ARE USED FOR:
            1. Authenticating Users
            2. Creating Users
    """

    # Simple route for basic testing
    @app.route('/myhome', methods=['GET'])
    def home():
        return "Hello World"

    # --- UNPROTECTED END-POINTS --- #
    # Login route
    @app.route('/authenticate', methods=['POST'])
    def login():
        response, code = authenticate_route(request)
        return jsonify(response), code

    # Registration route
    @app.route('/register', methods=['POST'])
    def register():
        response, code = registration_route(request)
        return jsonify(response), code

    #PROTECTED

    return app


# 200 successful GET 400 bad POST
# 201 Succesful POST 401 bad POST
