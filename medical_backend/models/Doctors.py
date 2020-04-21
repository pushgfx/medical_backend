from ..database import Database
from datetime import datetime,date, timedelta
import re
from ..models import User
db = Database()

class Doctor(User):

    def get_doctors(self):
        # Get a dictionary of all the doctors (names, id's)
        sql = "SELECT doctor_id, first_name, last_name FROM doctors"
        params = ()
        doctors = db.run_query(sql, params)

        return doctors

    def get_doctors_by_office(self, office_id):
        # Get a dictionary of all doctors for a specific office
        sql = "SELECT doctors.doctor_id, first_name, last_name, specialization_name,gender, phone, image FROM doctors, doctor_office_affiliations, specializations WHERE doctor_office_affiliations.office_id=%s AND doctor_office_affiliations.doctor_id=doctors.doctor_id AND specializations.specialist_id=doctors.specialist_id"
        params = (office_id)
        doctors = db.run_query(sql, params)

        return doctors

    def get_doctor_availability(self, office_id, doctor_id):
        # Get a dictionary of all availability for this doctor
        sql = "SELECT * FROM doctor_office_availability WHERE `doctor_id`=%s AND `office_id`=%s"
        params = (doctor_id, office_id)
        schedule = db.run_query(sql, params)
        return schedule

    def get_dates_dict(self, office_id, doctor_id, patient_id):
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
        sql = "SELECT appt_start_time, estimated_end_time, patient_id FROM appointments WHERE `doctor_id`=%s AND `office_id`=%s"
        params = (doctor_id, office_id)
        appointments = db.run_query(sql, params)

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
            for appointment in appointments:
                #print("\n")
                #print("appt_start_time.day %s future_date.day %s" % (appointment['appt_start_time'].day, future_date.day))
                #print("appointment[patient_id] = %s patient_id = %s" % (appointment['patient_id'], patient_id))
                if str(appointment['appt_start_time'].day) == str(future_date.day) and str(appointment['patient_id']) == str(patient_id):
                    print("\n")
                    print("This should be a disabled date")
                    date_check = True
                    break;
            if date_check == True:
                print("disabled date added %s %s %s" % (future_date.month, future_date.day, future_date.year))
                disabled_dates.append({"month":future_date.month,"day":future_date.day,"year":future_date.year})

        dates = {
            "av_dates": date_arr,
            "dis_dates": disabled_dates
        }

        return dates

    def get_doctor_patient(self,doctor_id):

        sql = """SELECT patients.patient_id,patients.first_name, patients.middle_initial, patients.last_name, patients.phone,patients.date_of_birth,patients.gender,patients.race
        FROM patients, patient_doctor_affiliation
        WHERE patient_doctor_affiliation.doctor_id=%s
        AND patient_doctor_affiliation.patient_id = patients.patient_id"""
        params = (doctor_id)
        results = db.run_query(sql, params)
        doctor_patient =[]
        for result in results:
            patient = {
                "patient_id":result['patient_id'],
                "firstName": result['first_name'],
                "middleInit": result['middle_initial'],
                "lastName": result['last_name'],
                "phone": result['phone'],
                "dob":result['date_of_birth'],
                "gender":result['gender'],
                "race":result['race']
            }
            doctor_patient.append(patient)
        print(doctor_patient)
        return doctor_patient

    def get_doctor_dict(self, doctor_id):
        sql = """SELECT doctors.*, specialization_name FROM doctors, specializations
        WHERE doctor_id=%s
        AND doctors.specialist_id = specializations.specialist_id"""
        params=(doctor_id)
        record = db.run_query(sql, params)
        result = record[0]
        profile = {
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
         "gender": result['gender'],
         "image": result['image']
        }
        return profile

    def get_doctor_all_appointment(self,doctor_id):

        # get curent datetime
        sql="SELECT appt_start_time from appointments where doctor_id=%s";
        params=(doctor_id)
        today_appointment_start_time = db.run_query(sql, params)

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

                result = db.run_query(sql, ())
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


    def get_today_appointments_by_doctor(self,doctor_id):
        current_date = datetime.now().date()
        sql="""SELECT appointments.appt_id,appointments.patient_id,
            CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
            offices.office_name AS office,
            appointments.was_referred, appointments.referring_doctor_id, appointments.appt_start_time,

            appointments.estimated_end_time,
            appointments.appt_status, appointments.booking_date, appointments.reason_for_visit
            FROM `appointments`,`offices`,`patients`
            WHERE DATE(appointments.appt_start_time) = %s
            AND appointments.doctor_id=%s AND offices.office_id=appointments.office_id
            AND appointments.patient_id=patients.patient_id
            AND (appointments.appt_status="pending" OR appointments.appt_status="started")
            ORDER BY appointments.appt_start_time DESC"""
        params=(current_date,doctor_id)
        result = db.run_query(sql,params)
        return result


    def get_past_appts_by_doctor(self,doctor_id):
        limit=30
        current_date = datetime.now().date()
        sql="""SELECT appointments.appt_id,appointments.patient_id,
            CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
            offices.office_name AS office,
            appointments.was_referred, appointments.referring_doctor_id, appointments.appt_start_time,

            appointments.estimated_end_time,
            appointments.appt_status, appointments.booking_date, appointments.reason_for_visit
            FROM `appointments`,`offices`,`patients`
            WHERE DATE(appointments.appt_start_time) < %s
            AND appointments.doctor_id=%s AND offices.office_id=appointments.office_id
            AND appointments.patient_id=patients.patient_id
            ORDER BY appointments.appt_start_time DESC
            LIMIT %s"""
        params=(current_date,doctor_id,limit)
        result = db.run_query(sql,params)
        return result

    def get_future_appts_by_doctor(self,doctor_id):
        current_date = datetime.now().date()
        sql="""SELECT appointments.appt_id,appointments.patient_id,
            CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
            offices.office_name AS office,
            appointments.was_referred, appointments.referring_doctor_id, appointments.appt_start_time,

            appointments.estimated_end_time,
            appointments.appt_status, appointments.booking_date, appointments.reason_for_visit
            FROM `appointments`,`offices`,`patients`
            WHERE DATE(appointments.appt_start_time) > %s
            AND appointments.doctor_id=%s AND offices.office_id=appointments.office_id
            AND appointments.patient_id=patients.patient_id
            AND (appointments.appt_status="pending")
            ORDER BY appointments.appt_start_time ASC"""
        params=(current_date,doctor_id)
        result = db.run_query(sql,params)
        return result

    def get_referred_appts_by_doctor(self,doctor_id):
        status="need approval"
        sql="""SELECT appointments.appt_id,appointments.patient_id, CONCAT(patients.first_name," ",patients.middle_initial, " ", patients.last_name) AS patient,
                        CONCAT(doctors.first_name," ",doctors.middle_initial, " ", doctors.last_name) AS doctor,
                        offices.office_name AS office, appointments.appt_status, appointments.appt_start_time,appointments.reason_for_visit
                        FROM `appointments`,`offices`,`patients`, `doctors`
                        WHERE appointments.referring_doctor_id=%s
                        AND offices.office_id=appointments.office_id
                        AND appointments.patient_id=patients.patient_id
                        AND appointments.doctor_id=doctors.doctor_id
                        AND appointments.appt_status=%s
                        ORDER BY appointments.appt_start_time ASC """
        params=(doctor_id,status)
        result = db.run_query(sql,params)
        return result

    def get_all_medications(self):
        sql = """SELECT * FROM medications"""
        result = db.run_query(sql, ())
        return result

    def get_all_medication_forms(self):
        sql = """SELECT * FROM medication_dose_forms"""
        result = db.run_query(sql, ())
        return result

    def update_doctor(self, request):
        doctor_id = request.json.get('doctorId')
        firstName = request.json.get('firstName')
        middleInit = request.json.get('middleInit')
        lastName = request.json.get('lastName')
        phone = request.json.get('phone')
        email = request.json.get('email')
        street = request.json.get('address')
        city = request.json.get('city')
        state = request.json.get('state')
        zipcode = request.json.get('zipcode')
        race = request.json.get('race')
        dob = request.json.get('dob')
        gender = request.json.get('gender')
        sql = """UPDATE doctors SET first_name=%s, middle_initial=%s, last_name=%s, phone=%s, email=%s, street_1=%s, city=%s, state=%s,zipcode=%s, race=%s, gender=%s WHERE doctor_id=%s"""
        params = (str(firstName), str(middleInit), str(lastName), str(phone), str(email),str(street),str(city),str(state),str(zipcode),str(race),str(gender), str(doctor_id))
        db.run_query(sql, params)

        return True


    def add_patient_prescription(self, request, doctor_id):
        appt_id = request.json.get("apptId", None)
        patient_id = request.json.get("patientId", None)
        medication_id = request.json.get("medicationId", None)
        dose_form_id = request.json.get("doseFormId", None)
        dosage = request.json.get("dosage", None)
        indication = request.json.get("indication", None)
        date_prescribed = request.json.get("datePrescribed", None)
        sql = "INSERT INTO `prescribed_medications` (appt_id,doctor_id,patient_id,medication_id,dose_form_id,dosage,indication,date_prescribed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        params = (str(appt_id), str(doctor_id), str(patient_id), str(medication_id), str(dose_form_id), str(dosage), str(indication),
                  str(date_prescribed))
        db.run_query(sql, params)

        return True

    def add_doctor(self, request):
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
        req_specialistId = request.json.get("specialistId", None)
        req_race = request.json.get("race", None)
        req_email = request.json.get("email", None)
        req_image = request.json.get("image", None)
        sql = "INSERT INTO `doctors` (`doctor_id`, `first_name`, `middle_initial`, `last_name`,`phone`, `specialist_id`,`gender`,`email`, `race`,`date_of_birth`, `street_1`, `city`, `state`, `zipcode`, `image` ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) "
        params = (
            str(req_first_name), str(req_middle_i), str(req_last_name),str(req_phone),str(req_specialistId),
            str(req_gender),str(req_email), str(req_race), str(req_dob), str(req_street_1), str(req_city),
            str(req_state),str(req_zipcode), str(req_image))

        db.run_query(sql, params)
        result = db.run_query("SELECT `doctor_id` FROM `doctors` ORDER BY `doctor_id` DESC LIMIT 1", ())
        uid = result[0]['doctor_id']
        today = date.today()
        self.add_user(req_email, request.json.get("password", None), 3, uid,today)
        
        return uid

    def get_specializations(self):
        # Get a dictionary of all the doctors (names, id's)
        sql = "SELECT * FROM specializations"
        params = ()
        specialization = db.run_query(sql, params)

        return specialization

    def add_patient_record(self, request, doctor_id):
        appt_id = request.json.get("apptId", None)
        patient_id = request.json.get("patientId", None)
        height = request.json.get("height", None)
        weight = request.json.get("weight", None)
        diagnoses = request.json.get("diagnoses", None)
        lab_testing = request.json.get("labTesting", None)
        treatment = request.json.get("treatment", None)
        new_prescriptions = request.json.get("newPrescriptions", None),
        actual_start_time= request.json.get("actualStartTime", None),
        actual_end_time = request.json.get("actualEndTime", None),
        sql = "INSERT INTO `medical_records` (appt_id,patient_id,doctor_id,height,weight,lab_testing,diagnoses,treatment,new_prescriptions,actual_start_time,actual_end_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params = (str(appt_id),str(patient_id),str(doctor_id),str(height),str(weight),lab_testing,str(diagnoses),str(treatment),new_prescriptions,actual_start_time,actual_end_time)
        db.run_query(sql, params)

        return True

    def get_appointment_doctor(self, patient_id):
        sql = """SELECT COUNT(*) as count from appointments WHERE patient_id=%s"""
        params = (str(patient_id))
        count = db.run_query(sql,params)
        count = count[0]
        #first appointment
        if count['count'] == 0:
            specialist_id=1
            sql = "SELECT doctors.specialist_id,doctors.doctor_id,doctors.first_name,doctors.middle_initial,doctors.last_name,specializations.specialization_name FROM doctors, specializations WHERE specialist_id=%s"
            params = (str(specialist_id))
            doctors = db.run_query(sql, params)

        else:
            sql = "SELECT doctors.specialist_id,doctors.doctor_id,doctors.first_name,doctors.middle_initial,doctors.last_name,specializations.specialization_name FROM doctors, specializations WHERE specializations.specialist_id=doctors.specialist_id"
            params = ()
            doctors = db.run_query(sql, params)

        return doctors

    def approve_specialist_appt(self,request):
        appt_id = request.json.get("appt_id", None)
        is_approve = request.json.get("is_approve", None)
        if is_approve:
            sql="""UPDATE `appointments` SET appt_status="pending" WHERE appt_id=%s"""
        else:
            sql = """UPDATE `appointments` SET appt_status="reject" WHERE appt_id=%s"""
        params = (appt_id)
        db.run_query(sql,params)

        return True


    def get_primary_physician(self):
        specialist_id=1
        sql = "SELECT doctor_id, first_name,middle_initial, last_name FROM doctors WHERE specialist_id=%s"
        params = (str(specialist_id))
        doctors = db.run_query(sql, params)

        return doctors

    def update_patient_prescription(self, request):
        rx_id = request.json.get('id')
        medication_name = request.json.get('medication_name')
        dosage = request.json.get('dosage')
        dose_form_name = request.json.get('dose_form_name')
        indication = request.json.get('indication')
        date_prescribed = request.json.get('date_prescribed')
        print(rx_id,medication_name, dosage, dose_form_name, indication, date_prescribed)
        sql = """UPDATE prescribed_medications
        SET dose_form_id=(select m.dose_form_id from medication_dose_forms m where m.dose_form_name=%s LIMIT 1),
        medication_id=(select m.medication_id from medications m where m.medication_name=%s LIMIT 1),
        indication = %s,dosage=%s,date_prescribed=%s WHERE id=%s """

        params = (str(dose_form_name),str(medication_name),str(indication),str(dosage),str(date_prescribed),str(rx_id))
        db.run_query(sql, params)
        return True

    def get_all_medications(self):
        sql ="SELECT * FROM medications"
        params=()
        return db.run_query(sql,params)

    def get_all_dose_forms(self):
        sql ="SELECT * FROM medication_dose_forms"
        params=()
        return db.run_query(sql,params)
