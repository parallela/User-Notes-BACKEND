from database import Database
import os
import datetime
from validator import Validator
from flask import jsonify
from flask_bcrypt import Bcrypt
from validate_email import validate_email


class DBHelpers:
    def __init__(self):
        self.database = Database()
        self.mysql = self.database.connection()
        self.dbprefix = os.getenv('DATABASE_PREFIX')

    def list_user_notes(self, user_id):
        self.mysql.execute("SELECT * FROM {}notes WHERE user_id={}".format(self.dbprefix, int(user_id)))
        result = self.mysql.fetchall()

        return result

    def see_note(self, user_id, note_slug):
        self.mysql.execute(
            "SELECT * FROM {}notes WHERE slug='{}' AND user_id={}".format(self.dbprefix, str(note_slug), int(user_id)))
        result = self.mysql.fetchone()

        return result

    def get_user(self, email):
        self.mysql.execute("SELECT * FROM {}users WHERE email='{}'".format(self.dbprefix, str(email)))
        result = self.mysql.fetchone()

        return result

    def get_user_data(self, user_id):
        self.mysql.execute(
            "SELECT id,username,created_at,email FROM {}users WHERE id={}".format(self.dbprefix, int(user_id)))
        result = self.mysql.fetchone()

        return result

    def check_if_user_exists(self, username, email):
        self.mysql.execute(
            "SELECT * FROM {}users WHERE `username`='{}' AND `email`='{}'".format(self.dbprefix, str(username),
                                                                                  str(email)))
        result = self.mysql.fetchone()

        if result is None:
            return True
        else:
            return False

    def register_user(self, username, email, password):
        verified = 0
        hash_password = Bcrypt().generate_password_hash(password, 12)
        email_valid = validate_email(email)
        password_lenght = len(password)
        date = datetime.datetime.now()
        validation_data = {'username': username, 'password': password}
        validation = Validator().validate_register_credentials(**validation_data)

        if email_valid:
            if validation == True:
                if self.check_if_user_exists(username, email):
                    self.mysql.execute(
                        "INSERT INTO `{}users` (`username`,`email`,`password`,`created_at`,`verified`) VALUES (%s,%s,%s,%s,%s)".format(
                            self.dbprefix),
                        (username, email, hash_password, date, verified))
                    return jsonify({"info": "Потребителят е създаден"}), 201
                else:
                    return jsonify({"error": "Потребителят съществува!"}), 401
            else:
                return validation
        else:
            return jsonify({"error": "Невалидна Е-Поща!"}), 401

    def get_user_statistics(self, user_id):
        user_private_notes = self.mysql.execute("SELECT * FROM {}notes WHERE public=0".format(self.dbprefix))
        user_public_notes = self.mysql.execute("SELECT * FROM {}notes WHERE public=1".format(self.dbprefix))
        user_amount_of_copies = self.mysql.execute("SELECT * from {}notes WHERE amount_of_copies>0".format(self.dbprefix))

        data_dict = dict(user_private_notes_amount=user_private_notes, user_public_notes_amount=user_public_notes,
                         user_note_copies=user_amount_of_copies)

        return data_dict
