from bcrypt import checkpw, gensalt, hashpw
from ..database import Database

db = Database()
cur = db.cur

class User:

	def check_user(self, email):
		sql = "SELECT * FROM `users` WHERE email=%s"
		params = (email)
		cur.execute(sql, params)
		result = cur.fetchone()
		return result

	def check_password(self, email, password):
		sql = "SELECT * FROM `users` WHERE email=%s"
		params = (email)
		cur.execute(sql, params)
		result = cur.fetchone()
		password_hash = result['password']
		print("password_hash before",password_hash)
		password_hash = password_hash.encode('utf-8')
		print("password_hash after",password_hash)

		print("password",password)
		print("password str" ,str(password))
		print("password str str",str.encode(str(password)))
		return checkpw(str.encode(password), password_hash)

	def add_user(self, email, password, role_id, user_id):
		hashed = hashpw(str.encode(password), gensalt(14))
		sql = "INSERT INTO `users` (`id`, `email`, `password`, `role_id`, `user_role_id`) VALUES (NULL, %s, %s, %s, %s)"
		params = (email,hashed,role_id,user_id)
		cur.execute(sql, params)
