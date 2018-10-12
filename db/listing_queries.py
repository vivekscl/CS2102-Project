from db import DatabaseCursor
from flask import current_app
import psycopg2

# This script contains all queries for the user table


def get_listing_by_id(listing_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listing with listing ID {} from database".format(listing_id))
        cursor.execute('select * from listing where listing_id = %s;', (listing_id,))
        return cursor.fetchone()


def insert_listing(owner_id, name, description, is_available=True):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO listing VALUES(DEFAULT, %s, %s, %s, %s);', (owner_id, name, description,
                                                                                    is_available))
            current_app.logger.info("Listing added to database: [{}, {}, {}, {}]"
                                    .format(owner_id, name, description, is_available))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}, {}, {}, {}]".format(owner_id, name, description, is_available))
        return False


def update_listing(listing_id, owner_id, name, description, is_available=True):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('UPDATE listing SET owner_id = %s, name = %s, description = %s, is_available = %s '
                           'where listing_id = %s;',
                           (owner_id, name, description, is_available, listing_id))
            current_app.logger.info("Listing {} updated: [{}, {}, {}, {}]"
                                    .format(listing_id, owner_id, name, description, is_available))
            return True
    except psycopg2.Error:
        current_app.logger.error("UPDATE FAILED: [{}, {}, {}, {}]".format(owner_id, name, description, is_available))
        return False


def delete_listing(listing_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Deleting listing {} from database".format(listing_id))
        cursor.execute("delete from listing where listing_id = %s", (listing_id,))


def get_listings_under_owner(owner_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under user with ID {}".format(owner_id))
        cursor.execute('select * from listing where owner_id = %s', (owner_id,))
        return cursor.fetchall()
