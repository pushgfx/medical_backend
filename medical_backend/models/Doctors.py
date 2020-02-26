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
		for d in range(30):
			future_date = current_date + timedelta(days=d)
			timeslots = ["avail","avail","avail","avail","avail","avail","avail","avail"]
			date_struct = {
				"datetime": datetime.strftime(future_date, "%m/%d/%Y"),
				"timeslots": timeslots
			}
			if future_date.isoweekday() < 6:
				date_arr.append(date_struct)


		# MARK BOOKED DATES/TIMESLOTS

		# add a query
		sql = "SELECT appt_start_time, estimated_end_time FROM appointments WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		# This is a dictionary of all appointments for this doctor_id
		appointments = cur.fetchall()
		for appointment in appointments:
			if appointment['appt_start_time'].day > current_date.day:
				for date in date_arr:
					if date["datetime"].hour == appointment['appt_start_time'].hour:
						slot = appointment['appt_start_time'].hour - 8
						date["timeslots"][slot - 1] = "booked"

		return dates
