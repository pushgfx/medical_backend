from ..database import Database
from datetime import datetime, timedelta

db = Database()
cur = db.cur

class Doctor:

	def get_dates_dict(self, doctor_id):
		# get curent datetime
		current_date = datetime.now()

		# FOR SAME DAY BOOKING...
		remaining_hours = 0
		# if before 4pm, calculate remaining hours for current work day
		if current_date.hour < 16:
			remaining_hours = 16 - current_date.hour
		# FOR SAME DAY BOOKING...


		date_arr = []
		for d in range(1,31): # We don't allow same day booking online
			future_date = current_date + timedelta(days=d)
			if future_date.isoweekday() < 7:
				timeslots = ["avail","avail","avail","avail","avail","avail","avail","avail"]
				date_struct = {
					"datetime": datetime.strftime(future_date, "%m/%d/%Y"),
					"timeslots": timeslots,
					"office_id": 0
				}
				date_arr.append(date_struct)

		# MARK BOOKED DATES/TIMESLOTS

		# Get a dictionary of all appointments for this doctor
		sql = "SELECT appt_start_time, estimated_end_time FROM appointments WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		appointments = cur.fetchall()

		# Get a dictionary of all availability for this doctor
		sql = "SELECT * FROM doctor_office_availability WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		schedule = cur.fetchall()

		# Gather unavailable timeslots from schedule dictionary
		uTimes = []
		for s in schedule:
			if s['is_available'] == "N":
				uTimes.append(s)

		# Filter out the taken dates
		for date in date_arr:
			for appointment in appointments:
				if appointment['appt_start_time'].day == date['datetime'].day:
					slot = appointment['appt_start_time'].hour - 8
					date["timeslots"][slot - 1] = "na"
			for uTime in uTimes:
				if uTime['day_of_week'] == date.isoweekday():
					sBeg = uTime['start_time'].hour - 8
					sEnd = uTime['end_time'].hour - 8
					n = sEnd - sBeg
					for x in range(n):
						sl = sBeg + x
						date['timeslots'][sl] = "na"
						date['office_id'] = 

		return date_arr