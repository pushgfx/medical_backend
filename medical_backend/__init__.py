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
        get_patient_route,
        get_doctor_dates,
        set_appointment_route
    )

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
    @app.route('/patients/authenticate', methods=['POST'])
    def login():
        response, code = authenticate_route(request)
        return jsonify(response), code

    # Registration route
    @app.route('/patients/register', methods=['POST'])
    def register():
        response, code = registration_route(request)
        print(response)
        return jsonify(response), code

    @app.route('/patients/profile', methods=['GET','PUT'])
    @jwt_required
    def patient_profile():
        response, code = get_patient_route(request)
        return jsonify(response), code

    @app.route('/doctors/dates', methods=['GET'])
    #@jwt_required
    def doctor_dates():
        response, code = get_doctor_dates(request)
        return jsonify(response), code

    @app.route('/patients/appointments', methods=['Post'])
    #@jwt_requiried
    def appointment():
        response, code = set_appointment_route(request)
        return jsonify(response), code

    
    
    return app
