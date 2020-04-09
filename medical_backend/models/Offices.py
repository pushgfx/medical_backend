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

	def update_office(self, office_id, office_name, street_1, city, state, zipcode, phone):
		sql = """UPDATE offices SET office_name=%s, street_1=%s, city=%s, state=%s, zipcode=%s, phone=%s WHERE office_id=%s """
		params = (str(office_name), str(street_1), str(city), str(state),str(zipcode), str(phone),office_id)
		db.run_query(sql, params)
		return True
	
