from database import Database
import os

class DBHelpers:
    def __init__(self):
        self.database = Database()
        self.mysql = self.database.connection()

    def list_user_notes(self,user_id):
        self.mysql.execute("SELECT * FROM {}notes WHERE user_id={}".format(os.getenv('DATABASE_PREFIX'),int(user_id)))
        result = self.mysql.fetchall()

        return result

    def see_note(self,note_slug):
        self.mysql.execute("SELECT * FROM {}notes WHERE slug='{}'".format(os.getenv('DATABASE_PREFIX'),str(note_slug)))
        result = self.mysql.fetchone()

        return result 