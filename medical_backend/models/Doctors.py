from ..database import Database
from datetime import datetime, timedelta

db = Database()
cur = db.cur

class Doctor:

	def get_doctors(self):
		# Get a dictionary of all the doctors (names, id's)
		sql = "SELECT doctor_id, first_name, last_name FROM doctors"
		cur.execute(sql)
		doctors = cur.fetchall()

		return doctors

	def get_doctor_availability(self, doctor_id):
		# Get a dictionary of all availability for this doctor
		sql = "SELECT * FROM doctor_office_availability WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		schedule = cur.fetchall()
		return schedule

	def get_dates_dict(self, doctor_id):
		# get curent datetime
		current_date = datetime.now()

		# FOR SAME DAY BOOKING...
		remaining_hours = 0
		# if before 4pm, calculate remaining hours for current work day
		if current_date.hour < 16:
			remaining_hours = 16 - current_date.hour
		# FOR SAME DAY BOOKING...

		# Build up an array for the next 30 days excluding Sundays
		date_arr = []
		for d in range(1,31): # We don't allow same day booking online
			future_date = current_date + timedelta(days=d)
			if future_date.isoweekday() < 7:
				date_struct = {
					"datetime": future_date,
					"timeslots": [],
					"office_id": 0
				}
				date_arr.append(date_struct)

		# MARK BOOKED DATES/TIMESLOTS

		# Get a dictionary of all appointments for this doctor
		sql = "SELECT appt_start_time, estimated_end_time FROM appointments WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		appointments = cur.fetchall()

		schedule = self.get_doctor_availability(doctor_id)

		# Filter out the taken dates
		for date in date_arr:
			for day in schedule:
				if str(date['datetime'].isoweekday()) == day['day_of_week']:
					date['timeslots'] = [day['timeslot_1'],day['timeslot_2'],day['timeslot_3'],day['timeslot_4'],day['timeslot_5'],day['timeslot_6'],day['timeslot_7'],day['timeslot_8']]
					date['office_id'] = day['office_id']
			for appointment in appointments:
				if appointment['appt_start_time'].day == date['datetime'].isoweekday():
					n = appointment['estimated_end_time'].hour - appointment['appt_start_time'].hour
					for x in range(n):
						slot = appointment['appt_start_time'].hour - 9
						date["timeslots"][slot + x] = "N"

		return date_arr

	def get_doctor_patient(self,doctor_id):
    
		sql = """SELECT patients.first_name, patients.middle_initial, patients.last_name, patients.phone
		FROM patients, patient_doctor_affiliation
		WHERE patient_doctor_affiliation.doctor_id=%s
		AND patient_doctor_affiliation.patient_id = patients.patient_id"""
		params = (doctor_id)
		cur.execute(sql,params)
		results = cur.fetchall()
		doctor_patient =[]
		for result in results:
			patient = {
				"firstName": result['first_name'],
				"middleInit": result['middle_initial'],
				"lastName": result['last_name'],
				"phone": result['phone']
			}
			doctor_patient.append(patient)
		return doctor_patient

	def get_doctor_dict(self,doctor_id):
		sql = """SELECT doctors.*, specialization_name FROM doctors, specializations
		WHERE doctor_id=%s
		AND doctors.specialist_id = specializations.specialist_id"""
		params=(doctor_id)
		cur.execute(sql,params)
		result = cur.fetchone()
		profile = {
		"firstName": result['first_name'],
		"middleInit": result['middle_initial'],
		"lastName": result['last_name'],
		"phone": result['phone'],
		"specialization_name": result['specialization_name']
		}
		return profile

	def get_doctor_all_appointment(self,doctor_id):

		# get curent datetime
		sql="SELECT appt_start_time from appointments where doctor_id=%s";
		params=(doctor_id)
		cur.execute(sql,params)
		today_appointment_start_time = cur.fetchall()

		current_date = datetime.now().date()
		appointments =[]

		for date in today_appointment_start_time:
			start_time = datetime.strptime(str(date['appt_start_time']), '%Y-%m-%d %X')
			if ( start_time.date() == current_date):
				sql="""SELECT appointments.appt_id,
					CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
					offices.office_name AS office,
					appointments.was_referred, appointments.referring_doctor_id, appointments.appt_start_time,
					appointments.estimated_end_time,
					appointments.appt_status, appointments.booking_date, appointments.reason_for_visit
					FROM `appointments`,`offices`,`patients`
					WHERE appointments.appt_start_time = %date"""

				cur.execute(sql)
				result = cur.fetchall()
				appointment = {
					"patient": result['patient'],
					"office": result['office'],
					"was_referred": result['was_referred'],
					"referring_doctor_id": result['referring_doctor_id'],
					"appt_start_time": result['appt_start_time'],
					"estimated_end_time": result['estimated_end_time'],
					"appt_status": result['appt_status'],
					"booking_date": result['booking_date'],
					"booking_method": result['booking_method'],
					"reason_for_visit": result['reason_for_visit']
					}
				appointments.append(appointment)
		return appointments