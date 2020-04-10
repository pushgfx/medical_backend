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
        get_all_doctors,
        get_doctors_by_office_route,
        get_doctor_dates,
        get_doctor_data_route,
        get_doctor_profile_route,
        get_doctor_appointments_route,
        get_offices_route,
        get_offices_by_doctor_route,
        get_admin_route,
        set_appointment_route,
        get_appointments_route,
        get_patient_rx_route,
        get_patient_records_route,
        delete_appt_route,
        update_offices_by_admin_route,
        get_Office_By_Id_route,
        insert_new_prescription_route,
    )

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
        return jsonify(response), code

    @app.route('/admin/profile', methods=['GET'])
    @jwt_required
    def admin_profile():
        response, code = get_admin_route(request)
        return jsonify(response), code

    @app.route('/patients/appointment', methods=['GET','POST'])
    @jwt_required
    def appointment():
        if request.method == 'GET':
            response, code = get_appointments_route(request)
        if request.method == 'POST':
            response, code = set_appointment_route(request)
        return jsonify(response), code

    @app.route('/patients/prescriptions', methods=['GET'])
    @jwt_required
    def patient_prescriptions():
        response, code = get_patient_rx_route(request)
        return jsonify(response), code

    @app.route('/patients/records', methods=['GET'])
    @jwt_required
    def patient_records():
        response, code = get_patient_records_route(request)
        return jsonify(response), code

    @app.route('/patients/profile', methods=['GET','PUT'])
    @jwt_required
    def patient_profile():
        response, code = get_patient_route(request)
        return jsonify(response), code

    @app.route('/doctors/dates', methods=['GET'])
    @jwt_required
    def doctor_dates():
        response, code = get_doctor_dates(request)
        return jsonify(response), code

    @app.route('/offices/doctor', methods=['GET'])
    @jwt_required
    def offices_doctors():
        response, code = get_offices_by_doctor_route(request)
        return jsonify(response), code

    @app.route('/doctor/data', methods=['GET'])
    @jwt_required
    def doctor_data():
        response, code = get_doctor_data_route()
        return jsonify(response), code

    @app.route('/doctors/list', methods=['GET'])
    @jwt_required
    def doctors():
        response, code = get_all_doctors()
        return jsonify(response), code

    @app.route('/doctors/office', methods=['GET'])
    def doctors_offices():
        response, code = get_doctors_by_office_route(request)
        return jsonify(response), code

    @app.route('/offices/list', methods=['GET'])
    def offices():
        response, code = get_offices_route()
        return jsonify(response), code


    @app.route('/doctor/profile', methods=['GET','PUT'])
    def doctor_profile():
        response, code = get_doctor_profile_route(request)
        return jsonify(response), code

    @app.route('/doctor/appointments', methods=['GET', 'PUT'])
    @jwt_required
    def doctor_appointments():
        response, code = get_doctor_appointments_route()
        return jsonify(response), code
    
    @app.route('/patient/deleteappointment', methods=['DELETE'])
    def delete_patient_appointments():
        response, code = delete_appt_route(request)
        return jsonify(response), code

    @app.route('/office/updateoffice' , methods = ['PUT'])
    def update_office():
        response, code = update_offices_by_admin_route(request)
        return jsonify(response), code
    
    @app.route('/offices/office' , methods = ['GET'])
    def get_Office_route ():
        response, code = get_Office_By_Id_route(request)
        return jsonify(response), code

    @app.route('/doctor/addprescription', methods=['POST'])
    def doctor_add_new_prescription():
        response, code = insert_new_prescription_route(request)
        return jsonify(response), code
    
    return app


