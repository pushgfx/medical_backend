from ..database import Database

db = Database()
cur = db.cur

class Appointments:

    def add_appointment(self,request,patient_id):
        
        req_patient_id= request.json.get("patient_id",None)
        req_office_id=request.json.get("office_id",None)
        req_doctor_id=request.json.get("doctor_id",None)
        req_was_reffered=request.json.get("was refered",None)
        req_was_reffered_by=request.json.get("refering doctor",None)
        req_appt_start_time=request.json.get("appointment start time",None)
        req_appt_end_time=request.json.get("appointment end time",None)
        req_appt_status=request.json.get("appointment status",None)
        req_appt_booking_date=request.json.get("booking date and time",None)
        req_appt_booking_method=request.json.get("booking method",None)
        req_reason_for_visit=request.json.get("reason for visit",None)
        
        sql="INSERT into `appointments`(`appt_id`,`patient_id`,`office_id`,`doctor_id`,`was_refered`,"\
        "`referring_doctor_id`,`appt_start_time`,`estimated_end_time`,`appt_status`,`booking_date`,"\
        "`booking_method`,`reason_for_visit`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (str(req_patient_id), str(req_office_id), str(req_doctor_id), str(req_was_reffered), str(req_was_reffered_by), str(req_appt_start_time), str(req_appt_end_time), str(req_appt_status), str(req_appt_booking_date), str(req_appt_booking_method), str(req_reason_for_visit))

        cur.execute(sql, params)