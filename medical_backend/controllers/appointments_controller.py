from ..models import Appointments
from flask_jwt_extended import get_jwt_claims, get_jwt_identity

def set_appointment_route(self,request):
   
    appointment = Appointments()
    patient_id = get_jwt_identity()['uid']
    appointment.add_appointment(request, patient_id)

    response, code = {"msg": "Set Appointment Success"}, 201
    return response, code