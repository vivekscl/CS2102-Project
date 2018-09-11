import psycopg2
from psycopg2 import extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config, Config
import os
from flask import current_app


class DatabaseCursor:
    """
    This class allows one to open a cursor using the 'with' keyword and perform the necessary SQL statements without
    having to explicitly commit changes.
    """
    def __enter__(self):
        self.db = connect_db()
        return self.db.cursor()

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()


def connect_db():
    conn_string = "host='localhost' dbname='cs2102' user='vivek'"  # Get port and password from .pgpass file
    conn = psycopg2.connect(conn_string, cursor_factory=extras.DictCursor)
    return conn


def init_db():
    # Create database first if it doesn't exist
    # postgres is the default db and can be used temporarily to interact with the db server and get useful info
    conn_string = "host='localhost' dbname='postgres' user='vivek'"
    conn = psycopg2.connect(conn_string)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    target_db = config[os.getenv("FLASK_CONFIG")].DATABASE_NAME

    # This command finds the database that we are creating, if it doesn't exist, the not_exist = None
    cur.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{}'".format(target_db))
    not_exists_row = cur.fetchone()
    not_exists = not_exists_row[0]

    if not_exists:
        cur.execute("CREATE DATABASE {};".format(target_db))

    # Create tables from schema.sql
    with DatabaseCursor() as cursor:
        cursor.execute(open(Config.SCHEMA_LOCATION, "r").read())


def insert_item(name, description, price):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO items VALUES(%s, %s, %s);', (name, description, price))
            current_app.logger.info("Item added to database: [{}, {}, {}]".format(name, description, price))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.info("INSERTION FAILED: [{}, {}, {}]".format(name, description, price))
        return False


def get_all_items():
    # Do note that the current_app can only be used within the context of a request, meaning that you can only use the
    # current_app variable if this method is being called during a request.
    current_app.logger.info("Getting all items from database")
    with DatabaseCursor() as cursor:
        cursor.execute('select * from items;')
        return cursor.fetchall()

