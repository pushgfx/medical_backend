from bcrypt import checkpw, gensalt, hashpw
from ..database import Database
from ..models import User

db = Database()


class Patient(User):

    def add_patient(self, request):
        req_first_name = request.json.get("firstName", None)
        req_middle_i = request.json.get("middleInit", None)
        req_last_name = request.json.get("lastName", None)
        req_street_1 = request.json.get("street", None)
        req_city = request.json.get("city", None)
        req_state = request.json.get("state", None)
        req_zipcode = request.json.get("zipcode", None)
        req_phone = request.json.get("phone", None)
        req_dob = request.json.get("dob", None)
        req_gender = request.json.get("gender", None)
        req_marital = request.json.get("marital", None)
        req_race = request.json.get("race", None)
        req_email = request.json.get("email", None)
        sql = "INSERT INTO `patients` (`patient_id`, `first_name`, `middle_initial`, `last_name`, `street_1`, `city`, " \
              "`state`, `zipcode`, `phone`, `date_of_birth`, `gender`, `marital_status`, `race`, `email`, " \
              "`primary_doctor`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL) "
        params = (
            str(req_first_name), str(req_middle_i), str(req_last_name), str(req_street_1), str(req_city),
            str(req_state),
            str(req_zipcode), str(req_phone), str(req_dob), str(req_gender), str(req_marital), str(req_race),
            str(req_email))
        db.run_query(sql, params)
        result = db.run_query("SELECT `patient_id` FROM `patients` ORDER BY `patient_id` DESC LIMIT 1", ())
        uid = result[0]['patient_id']
        self.add_user(req_email, request.json.get("password", None), 2, uid)
        return uid

    def update_patient(self, r, patient_id):
        sql = "UPDATE patients SET first_name=%s, middle_initial=%s, last_name=%s, street_1=%s, city=%s, state=%s, " \
              "zipcode=%s, phone=%s, date_of_birth=%s, gender=%s, marital_status=%s, race=%s, email=%s WHERE " \
              "patient_id=%s "
        params = (
            str(r.form['first_name']), str(r.form['middle_initial']), str(r.form['last_name']), str(r.form['street_1']),
            str(r.form['city']), str(r.form['state']), str(r.form['zipcode']), str(r.form['phone']), str(r.form['dob']),
            str(r.form['gender']), str(r.form['marital_status']), str(r.form['race']), str(r.form['email']), patient_id)
        db.run_query(sql, params)

    def get_patient_dict(self, patient_id):
        sql = "SELECT * FROM `patients` WHERE patient_id=%s"
        params = (patient_id,)
        patient = db.run_query(sql, params)
        result = patient[0]
        profile = {
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
            "race": result['race']
        }
        return profile

    def get_patient_appt_hist(self, patient_id):
        sql = "SELECT appointments.appt_id, appointments.appt_start_time, appointments.appt_status," \
              "appointments.booking_date," \
              "appointments.booking_method,doctors.first_name,doctors.last_name,offices.office_name " \
              "FROM appointments,doctors,offices " \
              "WHERE appointments.patient_id=%s " \
              " AND appointments.doctor_id=doctors.doctor_id " \
              " AND appointments.office_id=offices.office_id"
        params = (patient_id)
        appointments = db.run_query(sql, params)
        return appointments

    def get_patient_prescriptions(self, patient_id):
        sql = "SELECT PRESC.appt_id, D.first_name,D.last_name,MED.medication_name,PRESC.dosage,MED_FORM.dose_form_name, " \
              "PRESC.dosage,PRESC.indication,PRESC.date_prescribed " \
              "FROM doctors as D, medications as MED, medication_dose_forms as MED_FORM, prescribed_medications as PRESC " \
              "WHERE PRESC.patient_id=%s " \
              "AND PRESC.doctor_id=D.doctor_id " \
              "AND MED.medication_id=PRESC.medication_id " \
              "AND MED_FORM.dose_form_id=PRESC.dose_form_id"
        params = (patient_id)
        prescriptions = db.run_query(sql, params)
        return prescriptions


    def get_patient_records(self,patient_id):
        sql = "SELECT MR.*,D.first_name,D.last_name FROM medical_records as MR, doctors as D " \
              "WHERE MR.patient_id=%s AND MR.doctor_id = D.doctor_id"
        params = (patient_id)
        medical_records = db.run_query(sql, params)
        return medical_records
    
    def delete_appointment(self,appointment_id):
        sql = "DELETE FROM `appointments` WHERE (`appt_id` = '%s') AND (appt_status = `pending`)"
        params = (appointment_id)
        db.run_query(sql, params)
        return