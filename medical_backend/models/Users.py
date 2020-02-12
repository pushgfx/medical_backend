from ..database import Database
from bcrypt import checkpw, gensalt, hashpw

db = Database()
cur = db.cur

class User:

	def check_user(self, username):
		sql = "SELECT * FROM `users` WHERE username= '" + username + "'"
		cur.execute(sql)
		result = cur.fetchone()
		if not result:
			print("no existing user")
			return False
		else:
			print("existing user")
			return True

	def check_password(self, username, password):
		sql = "SELECT * FROM `users` WHERE username= '" + username + "'"
		cur.execute(sql)
		result = cur.fetchone()
		password_hash = result['password']
		return checkpw(str.encode(str(password)), password_hash)

	def add_user(self, username, password, role_id, user_id):
		print("add user entered")
		hashed = hashpw(str.encode(password), gensalt(14))
		sql = "INSERT INTO `users` (`id`, `username`, `password`, `role_id`, `user_role_id`) VALUES (NULL, %s, %s, %s, %s)"
		params = (username,password,role_id,user_id)
		cur.execute(sql, params)

	def add_client(self, r):
		hashed = hashpw(str.encode(str(r.form['password'])), gensalt(14))
		sql = "INSERT INTO `clients` (`client_id`, `first_name`, `middle_initial`, `last_name`, `street_1`, `city`, `state`, `zipcode`, `phone`, `date_of_birth`, `gender`, `marital_status`, `race`, `email`, `primary_doctor`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
		params = (str(r.form['first_name']),str(r.form['middle_initial']),str(r.form['last_name']),str(r.form['street_1']),str(r.form['city']),str(r.form['state']),str(r.form['zipcode']),str(r.form['phone']),str(r.form['dob']),str(r.form['gender']),str(r.form['marital_status']),str(r.form['race']),str(r.form['email']))
		cur.execute(sql, params)
		cur.execute("SELECT `client_id` FROM `clients` ORDER BY `client_id` DESC LIMIT 1")
		result = cur.fetchone()
		uid = result['client_id']
		self.add_user(r.form['username'], hashed, 2, uid)
		return uid

