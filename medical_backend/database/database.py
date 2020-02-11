import pymysql

class Database:
    def __init__(self):
        host = "199.19.77.230"
        user = "db_admin"
        password = "Password1"
        db = "medical_db"
      
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        self.cur = self.con.cursor()