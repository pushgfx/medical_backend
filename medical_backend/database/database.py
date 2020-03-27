import pymysql

class Database:
    def __init__(self):
        self.host = "199.19.77.230"
        self.user = "db_admin"
        self.password = "Password1"
        self.db = "medical_db"
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host, user=self.user, password=self.password, db=self.db, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            sys.exit()

    def run_query(self, query, params):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                if 'SELECT' in query:
                    cur.execute(query, params)
                    result = cur.fetchall()
                    cur.close()
                    return result
                else:
                    result = cur.execute(query, params)
                    self.conn.commit()
                    cur.close()

        except pymysql.MySQLError as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None