from ..database import Database
from datetime import datetime

db = Database()

class Appointments:

    def add_appointment(self,request,patient_id):
        
        sql = "SELECT * FROM patients WHERE patient_id=%s "
        params = (str(patient_id))
        result =  db.run_query(sql, params)
        mydoctor = False
        result = result[0]
        if result['primary_doctor'] is None:
            mydoctor = True

        req_patient_id = patient_id
        req_office_id = request.json.get("office", None)
        req_doctor_id = request.json.get("doctor", None)
        req_was_referred_by = request.json.get("refDoctor", None)
        req_date = request.json.get("date", None)
        req_timeslot = request.json.get("timeslot", None)
        req_appt_booking_method = request.json.get("bookingMethod", None)
        req_reason_for_visit = request.json.get("reason", None)
        current_dt = datetime.now()
        booking_date = current_dt
        year = int(req_date[0:4])
        month = req_date[5:7]
        if month[0] == "0":
            month = month[1]
        month = int(month)
        day = req_date[8:10]
        if day[0] == "0":
            day = day[1]
        day = int(day)
        hour = req_timeslot + 8
        appt_start_time = datetime(year, month, day, hour, minute=0, second=0, microsecond=0, tzinfo=None)
        appt_end_time = datetime(year, month, day, hour+1, minute=0, second=0, microsecond=0, tzinfo=None)
        appt_status = "pending"
        
        if req_was_referred_by == "0":
            columns = "`appt_id`,`patient_id`,`office_id`,`doctor_id`,`was_referred`,"\
            "`appt_start_time`,`estimated_end_time`,`appt_status`,`booking_date`,"\
            "`booking_method`,`reason_for_visit`"
            values = "NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
            params = (str(req_patient_id), str(req_office_id), str(req_doctor_id), "0", str(appt_start_time), str(appt_end_time), str(appt_status), str(booking_date), str(req_appt_booking_method), str(req_reason_for_visit))
        else:
            columns = "`appt_id`,`patient_id`,`office_id`,`doctor_id`,`was_referred`,"\
            "`referring_doctor_id`,`appt_start_time`,`estimated_end_time`,`appt_status`,`booking_date`,"\
            "`booking_method`,`reason_for_visit`"
            values = "NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
            params = (str(req_patient_id), str(req_office_id), str(req_doctor_id), "1", str(req_was_referred_by), str(appt_start_time), str(appt_end_time), str(appt_status), str(booking_date), str(req_appt_booking_method), str(req_reason_for_visit))

        sql = "INSERT into `appointments`(" + columns + ") VALUES (" + values + ")"
        db.run_query(sql, params)

        if mydoctor == True:
            sql = "UPDATE patients SET primary_doctor = %s WHERE patient_id=%s"
            params  = (str(req_doctor_id),str(req_patient_id))
            db.run_query(sql, params)


    def get_patient_appt_hist(self, patient_id):
        sql = """SELECT appointments.appt_id, appointments.appt_status, appointments.appt_start_time, appointments.booking_date, doctors.doctor_id,doctors.first_name, doctors.last_name FROM appointments, doctors WHERE appointments.patient_id=%s AND doctors.doctor_id=appointments.doctor_id ORDER BY appointments.appt_start_time DESC"""
        params = (patient_id)
        appointments = db.run_query(sql, params)

        return appointments