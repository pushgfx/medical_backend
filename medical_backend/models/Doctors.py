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
