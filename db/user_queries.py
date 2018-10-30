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


def insert_user(username, email, name, password, phone_no=None):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO users VALUES(DEFAULT, %s, %s, %s, %s, %s);', (username, email, name, password,
                                                                                      phone_no))
            current_app.logger.info("User added to database: [{}, {}, {}, {}, {}]".format(username, email, name,
                                                                                          password, phone_no))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.info("INSERTION FAILED: [{}, {}, {}, {}, {}]".format(username, email, name, password,
                                                                                phone_no))
        return False


def retrieve_users():
    with DatabaseCursor() as cursor:
        cursor.execute('select * from users')
        result = cursor.fetchall()
    return result
