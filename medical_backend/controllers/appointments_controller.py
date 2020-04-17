from ..models import Appointments
from flask_jwt_extended import get_jwt_claims, get_jwt_identity

def set_appointment_route(request):
   
    appointment = Appointments()
    patient_id = get_jwt_identity()['uid']
    appointment.add_appointment(request, patient_id)

    response, code = {"msg": "Set Appointment Success"}, 201
    return response, code

def get_appointments_route(request):

	appointment = Appointments()
	patient_id = get_jwt_identity()['uid']
	appointments = appointment.get_patient_appt_hist(patient_id)

	if appointments:
	    response, code = appointments, 200
	else:
		response, code = {"msg": "Bad Request"}, 400
	return response, code

def cancel_appt_route(request):
    appointment = Appointments()
    appt_id = request.json.get("appt_id", None)
    answer = appointment.cancel_appointment(appt_id)
	
    if answer:
        response, code = {"msg": "Cancel Successful"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400
    return response, code

# unused function
def update_finshed_appt_route(request):
    appointment= Appointments()
    appt_id = request.json.get("appt_id",None)
    appt_end_time = request.json.get("appt_end_time",None)
    answer = appointment.update_finished_appt(appt_id,appt_end_time)
    if answer:
        response, code ={"msg": "Appointment is successfully finished"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400

    return response, code

def update_appt_status_route(request):
    appointment= Appointments()
    appt_id = request.json.get("appt_id",None)
    status = request.json.get("appt_status", None)
    appt_end_time = request.json.get("timestamp",None)
    answer = appointment.update_appt_status(appt_id,appt_end_time,status)
    if answer:
        response, code ={"msg": "Appointment status is successfully updated"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400

    return response, code