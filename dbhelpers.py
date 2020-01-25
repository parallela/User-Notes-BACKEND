from database import Database
import os

class DBHelpers:
    def __init__(self):
        self.database = Database()
        self.mysql = self.database.connection()
        self.dbprefix = os.getenv('DATABASE_PREFIX')

    def list_user_notes(self,user_id):
        self.mysql.execute("SELECT * FROM {}notes WHERE user_id={}".format(self.dbprefix,int(user_id)))
        result = self.mysql.fetchall()

        return result

    def see_note(self,user_id,note_slug):
        self.mysql.execute("SELECT * FROM {}notes WHERE slug='{}' AND user_id={}".format(self.dbprefix,str(note_slug),int(user_id)))
        result = self.mysql.fetchone()

        return result

    def get_user(self,email):
        self.mysql.execute("SELECT * FROM {}users WHERE email='{}'".format(self.dbprefix, str(email)))
        result = self.mysql.fetchone()
        

        return result

    def get_user_data(self,user_id):
        self.mysql.execute("SELECT id,username,created_at,email FROM {}users WHERE id={}".format(self.dbprefix,int(user_id)))
        result = self.mysql.fetchone()

        return result       