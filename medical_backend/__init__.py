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
        get_doctor_admin_data_route,
        get_doctor_profile_route,
        get_doctor_appointments_route,
        get_offices_route,
        get_offices_by_doctor_route,
        get_admin_route,
        set_appointment_route,
        get_appointments_route,
        get_patient_rx_route,
        get_patient_records_route,
        cancel_appt_route,
        delete_appt_route,
        update_offices_by_admin_route,
        update_doctorprofile_route,
        insert_new_prescription_route,
        registration_doctor_route,
        get_all_specializations,
        update_patientprofile_route,
        insert_new_record_route,
        get_doctors_appointment,
        approve_specialist_appt_route,
        get_all_physician,
        get_admin_appointments_route,
        update_finshed_appt_route,
        update_appt_status_route,
        admin_reports_route
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
    
    # Registration route for doctor
    @app.route('/doctors/register', methods=['POST'])
    def doctor_register():
        response, code = registration_doctor_route(request)
        return jsonify(response), code

    @app.route('/admin/profile', methods=['GET'])
    @jwt_required
    def admin_profile():
        response, code = get_admin_route(request)
        return jsonify(response), code

    @app.route('/admin/appointments', methods=['GET'])
    @jwt_required
    def admin_appointments():
        response, code = get_admin_appointments_route()
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
    
    @app.route('/patient/cancel/appointment', methods=['POST'])
    @jwt_required
    def cancel_patient_appointment():
        response, code = cancel_appt_route(request)
        return jsonify(response), code

    @app.route('/admin/delete/appointment', methods=['POST'])
    @jwt_required
    def delete_patient_appointment():
        response, code = delete_appt_route(request)
        return jsonify(response), code

    @app.route('/office/updateoffice' , methods = ['PUT'])
    @jwt_required
    def update_office():
        response, code = update_offices_by_admin_route(request)
        return jsonify(response), code

    @app.route('/doctor/updatedoctor', methods = ['PUT'])
    @jwt_required
    def update_doctor():
        response, code = update_doctorprofile_route(request)
        return jsonify(response), code
        
    @app.route('/doctor/addprescription', methods=['POST'])
    @jwt_required
    def doctor_add_new_prescription():
        response, code = insert_new_prescription_route(request)
        return jsonify(response), code
    
    @app.route('/doctor/specialization', methods=['GET'])
    @jwt_required
    def get_specialization():
        response, code = get_all_specializations()
        return jsonify(response), code

    @app.route('/doctor/addrecord', methods=['POST'])
    @jwt_required
    def doctor_add_new_record():
        response, code = insert_new_record_route(request)
        return jsonify(response), code

    @app.route('/patient/updatepatient', methods = ['PUT'])
    @jwt_required
    def update_patient():
        response, code = update_patientprofile_route(request)
        return jsonify(response), code
    
    @app.route('/admin/doctor/data', methods=['GET'])
    @jwt_required
    def admin_doctor_data():
        response, code =  get_doctor_admin_data_route(request)
        return jsonify(response), code

    @app.route('/appointment/doctor/list', methods=['GET'])
    @jwt_required
    def appointment_doctor_data():
        response, code =  get_doctors_appointment(request)
        return jsonify(response), code

    @app.route('/doctor/approveappt', methods=['PUT'])
    @jwt_required
    def approve_specialist_appt():
        response, code = approve_specialist_appt_route(request)
        return jsonify(response), code
    
    @app.route('/doctor/physician/list', methods=['GET'])
    @jwt_required
    def get_doctor_physician():
        response, code =  get_all_physician(request)
        return jsonify(response), code

    # unused route
    @app.route('/doctor/finish/appointment', methods=['PUT'])
    @jwt_required
    def doctor_finished_appt():
        response, code = update_finshed_appt_route(request)
        return jsonify(response), code

    @app.route('/doctor/update/apptstatus', methods=['PUT'])
    @jwt_required
    def doctor_update_appt_status():
        response, code = update_appt_status_route(request)
        return jsonify(response), code

    @app.route('/admin/reports', methods=['POST'])
    @jwt_required
    def admin_reports():
        role = get_jwt_identity()['role']
        if role == 1:
            response, code = admin_reports_route(request)
        else:
            response, code = {"msg": "Must be admin"}, 401
        return jsonify(response), code

    return app



