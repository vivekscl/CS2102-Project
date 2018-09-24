from db import DatabaseCursor
from flask import current_app
import psycopg2

# This script contains all queries for the user table


def get_user_by_id(user_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting user with user ID {} from database".format(user_id))
        cursor.execute('select * from users where id = %s;', (user_id,))
        return cursor.fetchone()


def get_user_by_username(username):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting user with username {} from database".format(username))
        cursor.execute('select * from users where username = %s;', (username,))
        return cursor.fetchone()


def insert_user(username, name, password, phonenumber=None):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO users VALUES(DEFAULT, %s, %s, %s, %s);', (username, name, password, phonenumber))
            current_app.logger.info("User added to database: [{}, {}, {}, {}]"
                                    .format(username, name, password, phonenumber))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.info("INSERTION FAILED: [{}, {}, {}]".format(username, name, password, phonenumber))
        return False
