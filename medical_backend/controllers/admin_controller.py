from ..models import Admin, Doctor, Appointments

def get_admin_route(request):
	admin = Admin()
	doctor_profiles= admin.get_doctor_dict()
	patient_profiles= admin.get_patient_dict()
	appointments = admin.get_appointment_dict()
	offices = admin.get_office_dict()
	if doctor_profiles and patient_profiles and appointments and offices:
		response, code = {"doctors": doctor_profiles,"patients" : patient_profiles, "apointments": appointments, "offices": offices}, 200
	else:
		reponse, code = {"msg":"Bad admini request"}, 400

	return response, code

def get_doctor_admin_data_route(request):
	doctor = Doctor ()
	doctor_id = request.args.get('did')
	doctor_profile = doctor.get_doctor_dict(doctor_id)
	doctor_patient = doctor.get_doctor_patient(doctor_id)
	today_appointments=doctor.get_today_appointments_by_doctor(doctor_id)
	future_appointments=doctor.get_future_appts_by_doctor(doctor_id)
	past_appointments=doctor.get_past_appts_by_doctor(doctor_id)
	medication_names=doctor.get_all_medications()
	medication_forms=doctor.get_all_medication_forms()
	if doctor_profile:
		response, code = {"profile": doctor_profile, "patients": doctor_patient, "appointments":{"todayAppointments":today_appointments, "futureAppointments":future_appointments, "pastAppointments":past_appointments},"medications":{"medicationNames":medication_names,"medicationForms":medication_forms}}, 200
	else:
		response, code = {"msg": "Bad doctor id"}, 400

	return response, code

def delete_appt_route(request):
    appointment = Appointments()
    appt_id = request.json.get("appt_id", None)
    answer = appointment.delete_appointment(appt_id)
	
    if answer:
        response, code = {"msg": "Delete Successful"}, 200
    else:
        response, code = {"msg": "Bad Request"}, 400
    return response, code

def get_admin_appointments_route():
	admin = Admin()
	appointments = admin.get_appointment_dict()

	if appointments:
		response, code = {"appointments": appointments}, 200
	else:
		response, code = {"msg": "Error"}, 400
	return response, code

def admin_reports_route(request):
	admin = Admin()
	report = admin.get_report(request)
	if report:
		response, code = {"report": report}, 201
	else:
		response, code = {"msg": "No Report"}, 201
	return response, code