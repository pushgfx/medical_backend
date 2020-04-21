from bcrypt import checkpw, gensalt, hashpw
from ..database import Database
from ..models import User
from datetime import date

db = Database()

class Admin(User):
    def get_admin(self, id):
        sql = "SELECT * FROM admin where admin_id=%s"
        params=(id)
        admin = db.run_query(sql, params)
        return admin

    def get_doctor_dict(self):
        sql = """SELECT doctors.*,
        specializations.specialization_name
        FROM `doctors`, `specializations`
        WHERE doctors.specialist_id = specializations.specialist_id
        ORDER BY doctors.first_name"""
        results = db.run_query(sql, ())
        doctors =[]
        for result in results:
            doctor = {
                    "doctorId":result['doctor_id'],
                    "firstName": result['first_name'],
                    "middleInit": result['middle_initial'],
                    "lastName": result['last_name'],
                    "phone": result['phone'],
                    "specializationName": result['specialization_name'],
                    "street": result['street_1'],
                    "city": result['city'],
                    "state": result['state'],
                    "zipcode": result['zipcode'],
                    "race": result['race'],
                    "email": result['email'],
                    "dob": result['date_of_birth'],
                    "gender": result['gender']
                }
            doctors.append(doctor)
        return doctors

    def get_patient_dict(self):
        sql = "SELECT * FROM `patients` ORDER BY first_name"
        results = db.run_query(sql, ())
        patients =[]
        for result in results:
            patient = {
                "patientId": result['patient_id'],
                "firstName": result['first_name'],
                "middleInit": result['middle_initial'],
                "lastName": result['last_name'],
                "street": result['street_1'],
                "city": result['city'],
                "state": result['state'],
                "zipcode": result['zipcode'],
                "phone": result['phone'],
                "dob": result['date_of_birth'],
                "gender": result['gender'],
                "marital": result['marital_status'],
                "race": result['race'],
                "email": result['email'],
                "primary_doctor": result['primary_doctor']
                }
            patients.append(patient)
        return patients

    def get_appointment_dict(self):
        sql = """(SELECT
                appointments.appt_id,
                CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
                CONCAT(d1.first_name," ",d1.middle_initial, " ", d1.last_name) AS doctor,
                offices.office_name AS office,
                appointments.was_referred,appointments.referring_doctor_id as referring_doctor, appointments.appt_start_time, appointments.estimated_end_time,
                appointments.appt_status, appointments.booking_date, appointments.booking_method, appointments.reason_for_visit
                FROM `appointments`, `doctors` as d1,  `offices`,`patients`
                WHERE appointments.patient_id = patients.patient_id AND
                appointments.doctor_id = d1.doctor_id AND
                appointments.office_id = offices.office_id AND
                appointments.referring_doctor_id is null)
                UNION
                (SELECT
                appointments.appt_id,
                CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
                CONCAT(d1.first_name," ",d1.middle_initial, " ", d1.last_name) AS doctor,
                offices.office_name AS office,
                appointments.was_referred,CONCAT(d2.first_name," ",d2.middle_initial, " ", d2.last_name) AS referring_doctor,
                 appointments.appt_start_time, appointments.estimated_end_time,
                appointments.appt_status, appointments.booking_date, appointments.booking_method, appointments.reason_for_visit
                FROM `appointments`, `doctors` as d1, `doctors` as d2, `offices`,`patients`
                WHERE appointments.patient_id = patients.patient_id AND
                appointments.doctor_id = d1.doctor_id AND
                appointments.office_id = offices.office_id AND
                appointments.referring_doctor_id = d2.doctor_id);"""

        results = db.run_query(sql, ())
        appointments=[]
        for result in results:
            if result['was_referred']==0:
                result['was_referred']="NO"
            else:
                result['was_referred']="YES"
            appt = {
                "appointmentId": result['appt_id'],
                "patient": result['patient'],
                "doctor": result['doctor'],
                "office": result['office'],
                "was_referred": result['was_referred'],
                "referring_doctor": result['referring_doctor'],
                "appt_start_time": result['appt_start_time'],
                "estimated_end_time": result['estimated_end_time'],
                "appt_status": result['appt_status'],
                "booking_date": result['booking_date'],
                "booking_method": result['booking_method'],
                "reason_for_visit": result['reason_for_visit']
                }
            appointments.append(appt)
        return appointments

    def get_office_dict(self):
        sql = "SELECT * FROM `offices`"
        results = db.run_query(sql, ())
        offices =[]
        for result in results:
            office = {
                "office_id": result ['office_id'],
                "office_name": result['office_name'],
                "street_1": result['street_1'],
                "city": result['city'],
                "state": result['state'],
                "zipcode": result['zipcode'],
                "phone": result['phone']
                }
            offices.append(office)
        return offices

    def add_doctor(self):
        req_first_name = request.json.get("firstName", None)
        req_middle_i = request.json.get("middleInit", None)
        req_last_name = request.json.get("lastName", None)
        req_phone = request.json.get("phone", None)
        req_spec = request.json.get("specialization_name", None)
        req_email = request.json.get("email", None)

        sql = """ INSERT INTO `doctors` (`doctor_id`, `first_name`, `middle_initial`, `last_name`, `phone`,
        specialist_id) VALUES (NULL, %s, %s, %s, %s, %s) """
        params = (
            str(req_first_name), str(req_middle_i), str(req_last_name), str(req_phone), str(req_spec))

        cur.execute(sql, params)
        cur.execute("SELECT `doctor_id` FROM `doctors` ORDER BY `doctor_id` DESC LIMIT 1")
        result = cur.fetchone()
        uid = result['doctor_id']
        self.add_user(req_email, str(uid) +req_last_name, 3, uid)
        return uid

    def update_doctor(self, r, doctor_id):
        sql = """UPDATE doctors SET first_name=%s, middle_initial=%s, last_name=%s, phone=%s, specialist_id=%s, email=%s
                    WHERE doctors=%s """
        params = (
            str(r.form['first_name']), str(r.form['middle_initial']), str(r.form['last_name']), str(r.form['phone']),
             str(r.form['specialization_id']),str(r.form['email']), doctor_id)
        db.run_query(sql, params)
        return True

    def get_report(self, request):
        reportType = request.json.get('reportType', None)
        patient = request.json.get('patient', None)
        doctor = request.json.get('doctor', None)
        office = request.json.get('office', None)
        result=[]
        if reportType == "Canceled Appointments":
            condition = "WHERE appt_status='canceled' AND a.patient_id=p.patient_id AND a.doctor_id=d.doctor_id AND a.office_id=o.office_id"
            if patient != "all":
                condition += " AND a.patient_id=" + str(patient)
            if doctor != "all":
                condition += " AND a.doctor_id=" + str(doctor)
            if office != "all":
                condition += " AND a.office_id=" + str(office)

            sql = "SELECT a.appt_id, a.doctor_id, a.office_id, a.patient_id, p.first_name, p.middle_initial, p.last_name, o.office_name, \
            d.first_name as doc_first_name, d.middle_initial as doc_middle_initial, d.last_name as doc_last_name, a.appt_start_time, a.estimated_end_time, \
            a.appt_status, a.booking_date, a.booking_method, a.reason_for_visit \
            FROM appointments as a, patients as p, doctors as d, offices as o " + condition
            params = ()
            result = db.run_query(sql, params)

            labels = ["Appointment ID", "Patient", "Office", "Doctor", "Start Time", "End Time", "Status",
                      "Booking Date", "Booking Method", "Reason for Visit"]
        elif reportType == "Average Appointment Duration":
            condition = "WHERE a.appt_status='finished' AND a.doctor_id=d.doctor_id"
            if office !="all":
                condition += "AND o.office_id=" + str(office)
            sql = "SELECT a.doctor_id,d.first_name,d.last_name, COALESCE(AVG(TIME_TO_SEC(TIMEDIFF(actual_end_time,actual_start_time)))/60,0) AS avg_appt_duration FROM appointments as a, doctors as d " + condition +"GROUP BY d.doctor_id"
            params = ()
            result = db.run_query(sql, params)

        return result
    
    def get_user_report(self,request):
        result = []
        role_id = request.json.get('roleId', None)

        req_firstDate = request.json.get("firstDate", None)
        req_secondDate = request.json.get("secondDate", None)
        
        month = req_firstDate[4:7]
        day = req_firstDate[8:10]
        year = req_firstDate[11:15]
        
        if(month == "Jan"):
            month = "01"
        elif(month == "Feb"):
            month = "02"
        elif(month == "Mar"):
            month = "03"
        elif(month == "Apr"):
            month = "04"
        elif(month == "May"):
            month = "05"
        elif(month == "Jun"):
            month = "06"
        elif(month == "Juy"):
            month = "07"
        elif(month == "Aug"):
            month = "08"
        elif(month == "Sep"):
            month = "09"
        elif(month == "Oct"):
            month = "10"
        elif(month == "Nov"):
            month = "11"
        elif(month == "Dec"):
            month = "12"


        selected_first_date = str(year) + "-" + str(month) + "-" + str(day)
        month = req_secondDate[4:7]
        day = req_secondDate[8:10]
        year = req_secondDate[11:15]
        if(month == "Jan"):
            month = "01"
        elif(month == "Feb"):
            month = "02"
        elif(month == "Mar"):
            month = "03"
        elif(month == "Apr"):
            month = "04"
        elif(month == "May"):
            month = "05"
        elif(month == "Jun"):
            month = "06"
        elif(month == "Juy"):
            month = "07"
        elif(month == "Aug"):
            month = "08"
        elif(month == "Sep"):
            month = "09"
        elif(month == "Oct"):
            month = "10"
        elif(month == "Nov"):
            month = "11"
        elif(month == "Dec"):
            month = "12"
        selected_last_date = str(year) + "-" + str(month) + "-" + str(day)

        
        if role_id != "all":
            sql = "SELECT COUNT(*) AS count FROM users WHERE role_id=%s AND date_account_created >='" +selected_first_date+ "' AND date_account_created <= '" + selected_last_date + "'"
            params = (str(role_id))
            result = db.run_query(sql, params)
            result = result[0]

            sql = "SELECT email,date_account_created,role_name FROM users,roles WHERE users.role_id=%s AND roles.role_id=users.role_id AND date_account_created >='" +selected_first_date+ "' AND date_account_created <= '" + selected_last_date + "'"
            params = (str(role_id))
            result_2 = db.run_query(sql, params)

        else:
            sql = "SELECT COUNT(*) AS count FROM users WHERE date_account_created >='" +selected_first_date+ "' AND date_account_created <= '" + selected_last_date + "'"
            result = db.run_query(sql,())
            result = result[0]
            sql = "SELECT email,date_account_created,role_name FROM users,roles WHERE users.role_id=roles.role_id AND date_account_created >='" +selected_first_date+ "' AND date_account_created <= '" + selected_last_date + "'"
            result_2 = db.run_query(sql, ())
    
        
        return result,result_2