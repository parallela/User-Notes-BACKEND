import pymysql
import pymysql.cursors
import os
import logging
import sys

class Database:
    def __init__(self):
        # DB logging
        logging.basicConfig(filename="db.log")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.db = self.connection()

    def connection(self):
        host = os.getenv('DATABASE_HOST')
        username = os.getenv('DATABASE_USERNAME')
        password = os.getenv('DATABASE_PASSWORD')
        db = os.getenv('DATABASE_DB')

        try:
            con = pymysql.connect(host=host, user=username, password=password, db=db)
            cursor = con.cursor(pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            self.logger.error("{!r}, {}".format(e,e.args[0]))
            sys.exit(1)

        return cursor