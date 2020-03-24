from ..database import Database

db = Database()
cur = db.cur

class Office:

	def get_all_offices(self): 
		sql = "SELECT * FROM offices" 
		cur.execute(sql)
		offices = cur.fetchall()

		return offices

	def get_offices_by_doctor(self, doctor_id):
		sql = "SELECT office_id FROM doctor_office_affiliations WHERE `doctor_id`=%s"
		params = (doctor_id)
		cur.execute(sql, params)
		oids = cur.fetchall()
		off_ids = []
		for oid in oids:
			off_ids.append(oid["office_id"])
		tuple_list = "("
		for x in off_ids:
			tuple_list += "%s"
		tuple_list += ")"

		sql = "SELECT * FROM offices WHERE `office_id` in " + tuple_list
		params = tuple(off_ids)
		cur.execute(sql, params)
		offices = cur.fetchall()
		
		return offices