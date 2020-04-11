from ..database import Database

db = Database()

class Office:

	def get_all_offices(self): 
		sql = "SELECT * FROM offices" 
		params = ()
		offices = db.run_query(sql, params)

		return offices

	def get_offices_by_doctor(self, doctor_id):
		sql = "SELECT * FROM offices, doctor_office_affiliations WHERE doctor_office_affiliations.doctor_id=%s AND doctor_office_affiliations.office_id=offices.office_id"
		params = (doctor_id)
		offices = db.run_query(sql, params)
		
		return offices

	def update_office(self, request):
		payload = request.get_json()['payload']
		office_id = payload['oid']
		office_name = payload['oname']
		office_street = payload['address']
		office_city = payload['city']
		office_state = payload['state']
		office_zipcode = payload['zipcode']
		office_phone = payload['phone']

		sql = """UPDATE offices SET office_name=%s, street_1=%s, city=%s, state=%s, zipcode=%s, phone=%s WHERE office_id=%s """
		params = (str(office_name), str(office_street), str(office_city), str(office_state),str(office_zipcode), str(office_phone),office_id)
		db.run_query(sql, params)
		return True
	
