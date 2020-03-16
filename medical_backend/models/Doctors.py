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

	def get_offices(self, doctor_id):
		sql = "SELECT office_id FROM doctor_office_affiliations WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		oids = cur.fetchall()
		off_ids = []
		for oid in oids:
			off_ids.append(oid["office_id"])
		print(off_ids)
		tuple_list = "("
		for x in off_ids:
			tuple_list += "%s"
		tuple_list += ")"

		sql = "SELECT * FROM offices WHERE `office_id` in " + tuple_list
		params = tuple(off_ids)
		cur.execute(sql, params)
		offices = cur.fetchall()
		return offices

	def get_doctor_availability(self, office_id, doctor_id):
		# Get a dictionary of all availability for this doctor
		sql = "SELECT * FROM doctor_office_availability WHERE `doctor_id`=%s AND `office_id`=%s"
		params = (doctor_id, office_id)
		cur.execute(sql, params)
		schedule = cur.fetchall()
		return schedule

	def get_dates_dict(self, office_id, doctor_id):
		# get curent datetime
		current_date = datetime.now()
		# Build up an array for the next 30 days excluding Sundays
		date_arr = []
		disabled_dates = []
		for d in range(1,31): # We don't allow same day booking online
			future_date = current_date + timedelta(days=d)
			weekday = future_date.isoweekday()
			timeslots  = ["Y","Y","Y","Y","Y","Y","Y","Y"]
			if weekday == 7:
				timeslots = ["N","N","N","N","N","N","N","N"]
			date_struct = {
				"datetime": {"month":future_date.month,"day":future_date.day,"year":future_date.year,"weekday":weekday},
				"timeslots": timeslots,
				"office_id": 0
			}
			date_arr.append(date_struct)

		# MARK BOOKED DATES/TIMESLOTS

		# Get a dictionary of all appointments for this doctor
		sql = "SELECT appt_start_time, estimated_end_time FROM appointments WHERE `doctor_id`=%s AND `office_id`=%s"
		params = (doctor_id, office_id)
		cur.execute(sql, params)
		appointments = cur.fetchall()

		schedule = self.get_doctor_availability(office_id, doctor_id)

		# Filter out the taken dates
		for date in date_arr:
			for day in schedule:
				if str(date['datetime']['weekday']) == day['day_of_week']:
					date['timeslots'] = [day['timeslot_1'],day['timeslot_2'],day['timeslot_3'],day['timeslot_4'],day['timeslot_5'],day['timeslot_6'],day['timeslot_7'],day['timeslot_8']]
					date['office_id'] = day['office_id']
			for appointment in appointments:
				if appointment['appt_start_time'].day == date['datetime']['day']:
					n = appointment['estimated_end_time'].hour - appointment['appt_start_time'].hour
					for x in range(n):
						slot = appointment['appt_start_time'].hour - 9
						date["timeslots"][slot + x] = "N"
		for d in range(0,30):
			future_date = current_date + timedelta(days=d+1)
			date_check = True
			for timeslot in date_arr[d]['timeslots']:
				if timeslot == "Y":
					date_check = False
					break
			if date_check == True:
				disabled_dates.append({"month":future_date.month,"day":future_date.day,"year":future_date.year})

		dates = {
		    "av_dates": date_arr,
		    "dis_dates": disabled_dates
		}

		return dates

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