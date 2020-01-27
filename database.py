import pymysql
import pymysql.cursors
import os
import logging
import sys


class Database:
    def __init__(self):
        self.db = self.connection()

    def connection(self):
        host = os.getenv('DATABASE_HOST')
        username = os.getenv('DATABASE_USERNAME')
        password = os.getenv('DATABASE_PASSWORD')
        db = os.getenv('DATABASE_DB')

        try:
            con = pymysql.connect(host=host, user=username, password=password, db=db, autocommit=True)
            cursor = con.cursor(pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            sys.exit(1)

        return cursor
