import pymysql
import pymysql.cursors

class Database:
    def __init__(self):
        host = "127.0.0.1"
        username = "root"
        password = "parola"
        db = "usernotes"

        self.notes_table = "usernotes_notes"
        self.user_table = "usernotes_users"

        self.con = pymysql.connect(host=host, user=username, password=password, db=db)
        self.cursor = self.con.cursor()

    def list_user_notes(self,user_id):
        self.cursor.execute("SELECT * FROM {} WHERE user_id={}".format(self.notes_table,user_id))
        result = self.cursor.fetchall()

        return result