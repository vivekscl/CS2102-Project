from db import DatabaseCursor
from flask import current_app
import psycopg2

# This script contains all queries for the tag table

def get_all_tags():
    with DatabaseCursor() as cursor:
        cursor.execute('SELECT * FROM tag;')
        return cursor.fetchall()

def get_tag_by_id(tag_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting tag with tag ID {} from database".format(tag_id))
        cursor.execute('select * from tag where tag_id = %s;', (tag_id,))
        return cursor.fetchone()

def insert_tag(name):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO tag VALUES(DEFAULT, %s);', name)
            current_app.logger.info("Tag added to database: [{}]"
                                    .format(name))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}]".format(name))
        return False


def update_tag(tag_id, name):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('UPDATE tag SET name = %s'
                           'where tag_id = %s;',
                           (name, tag_id))
            current_app.logger.info("Tag {} updated: [{}]"
                                    .format(tag_id, name))
            return True
    except psycopg2.Error:
        current_app.logger.error("UPDATE FAILED: [{}, {}]".format(tag_id, name))
        return False


def delete_tag(tag_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Deleting tag {} from database".format(tag_id))
        cursor.execute("delete from tag where tag_id = %s", tag_id)


def get_listings_by_tag_name(tag_name):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under tag with name {}".format(tag_name))
        cursor.execute('SELECT * FROM listing WHERE listing_id IN '
                       '(SELECT listing_id FROM listing_tag WHERE tag_id = (SELECT tag_id FROM tag WHERE name = %s));', (tag_name,))
        return cursor.fetchall()

def insert_listing_tag(tag_id, listing_name, owner_id):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO listing_tag VALUES(%s, %s, %s);', (tag_id, listing_name, owner_id))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("listing_tag insertion failed: [{}]".format(tag_id))
        return False
