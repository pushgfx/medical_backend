from bcrypt import checkpw, gensalt, hashpw
from ..database import Database

db = Database()
cur = db.cur

class User:

	def check_user(self, username):
		sql = "SELECT * FROM `users` WHERE username= '" + username + "'"
		cur.execute(sql)
		result = cur.fetchone()
		return result

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

