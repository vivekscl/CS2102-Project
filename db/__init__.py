import psycopg2
from psycopg2 import extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config, Config
import os


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
    conn_string = config[os.getenv("FLASK_CONFIG")].CONNECTION_FILE
    conn = psycopg2.connect(conn_string, cursor_factory=extras.DictCursor)
    return conn


def init_db(): 
    """
    Create database first if it doesn't exist
    postgres is the default db and can be used temporarily to interact with the db server and get useful info
    """
    conn_string = config[os.getenv("FLASK_CONFIG")].CONNECTION_FILE
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

