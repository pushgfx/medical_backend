from ..database import Database

db = Database()
cur = db.cur

class Offices:

	def get_offices(self):
		# Get a dictionary of all the doctors (names, id's)
		sql = "SELECT * FROM offices"
		cur.execute(sql)
		offices = cur.fetchall()

		return offices