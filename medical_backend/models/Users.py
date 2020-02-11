from ..database import Database
from bcrypt import checkpw, gensalt, hashpw

db = Database()
cur = db.cur

class User:
	def getUserById(id):
		sql = 'SELECT * FROM users WHERE id = ' + id
		cur.execute(sql)
		result = cur.fetchone()
		return result

	def check_password(username, password):
		sql = 'SELECT password FROM users WHERE username = ' + username
		cur.execute(sql)
		result = cur.fetchone()
		password_hash = result.password
		return checkpw(str.encode(password), password_hash)

	def add_user(username,password,role_id):
		hashed = hashpw(str.encode(password), gensalt(14))
		sql = 'INSERT username, hashed, role_id INTO users'
		cur.execute(sql)
