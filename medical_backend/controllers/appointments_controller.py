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

def update_finshed_appt_route(request):
    appointment= Appointments()
    appt_id = request.json.get("appt_id",None)
    appt_end_time = request.json.get("appt_end_time",None)
    print("APPT_ID",appt_id)
    print("APPT_END_TIme",appt_end_time)

    answer = appointment.update_finished_appt(appt_id,appt_end_time)
    print("FINISHED 2",answer)
    if answer:
        response, code ={"msg": "Appointment is successfully finished"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400

    return response, code