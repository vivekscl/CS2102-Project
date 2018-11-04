from db import DatabaseCursor
from flask import current_app
import psycopg2

# This script contains all queries for the user table


def get_listing(listing_name, owner_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listing {} from owner {} from database".format(listing_name, owner_id))
        cursor.execute('select * from listing where listing_name = %s and owner_id = %s;', (listing_name, owner_id))
        return cursor.fetchone()


def get_all_listing():
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting all listing from database".format())
        cursor.execute('SELECT * FROM LISTING;')
        return cursor.fetchall()


def insert_listing(listing_name, owner_id, description, listed_date, is_available=True):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO listing VALUES(%s, %s, %s, %s, %s);', (listing_name, owner_id, description,
                                                                               listed_date, is_available))
            current_app.logger.info("Listing {} added to database: [{}, {}, {}, {}]"
                                    .format(listing_name, owner_id, description, listed_date, is_available))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION of {} FAILED: [{}, {}, {}, {}]".format(listing_name, owner_id, description,
                                                                                   listed_date, is_available))
        return False


def update_listing(listing_name, owner_id, description, listed_date, is_available=True):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('UPDATE listing SET listed_date = %s, description = %s, is_available = %s '
                           'where listing_name = %s and owner_id = %s;',
                           (listed_date, description, is_available, listing_name, owner_id))
            current_app.logger.info("Listing {} updated: [{}, {}, {}, {}]"
                                    .format(listing_name, description, is_available, listed_date, owner_id))
            return True
    except psycopg2.Error:
        current_app.logger.error("UPDATE FAILED: [{}, {}, {}, {}, {}]".format(listed_date, description, is_available,
                                                                              listing_name, owner_id))
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


# for search queries by listing name
def get_listings_by_listing_name(listing_name):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under listing with name {}".format(listing_name))
        cursor.execute("SELECT l.listing_name, u.name AS user_name, l.description, l.listed_date, "
                       "tag.name AS tag_name, l.owner_id FROM listing l "
                       "LEFT JOIN listing_tag lt ON l.listing_name = lt.listing_name AND l.owner_id = lt.owner_id  "
                       "LEFT JOIN tag AS tag ON lt.tag_id = tag.tag_id "
                       "LEFT JOIN users AS u ON l.owner_id = u.id "
                       "WHERE LOWER(l.listing_name) LIKE LOWER(%s) "
                       "GROUP BY l.listing_name, u.name, l.description, l.listed_date, tag.name, l.owner_id "
                       "ORDER BY listed_date DESC;",
                       (listing_name,))
        return cursor.fetchall()


# for search queries by tag name
def get_listings_by_tag_name(tag_name):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under tag with name {}".format(tag_name))
        cursor.execute("SELECT l.listing_name, u.name AS user_name, l.description, l.listed_date, "
                       "tag.name AS tag_name, l.owner_id FROM listing l "
                       "LEFT JOIN listing_tag lt ON l.listing_name = lt.listing_name AND l.owner_id = lt.owner_id  "
                       "LEFT JOIN tag AS tag ON lt.tag_id = tag.tag_id "
                       "LEFT JOIN users AS u ON l.owner_id = u.id "
                       "WHERE l.listing_name IN (SELECT lt2.listing_name FROM listing_tag lt2 "
                       "WHERE tag_id IN (SELECT tag2.tag_id FROM tag tag2 WHERE LOWER(name) LIKE LOWER(%s))) "
                       "AND l.owner_id IN (SELECT lt2.owner_id FROM listing_tag lt2 "
                       "WHERE tag_id IN (SELECT tag2.tag_id FROM tag tag2 WHERE LOWER(name) LIKE LOWER(%s)))"
                       "GROUP BY l.listing_name, u.name, l.description, l.listed_date, tag.name, l.owner_id "
                       "ORDER BY listed_date DESC;",
                       (tag_name, tag_name,))
        return cursor.fetchall()


# for search queries by owner name
def get_listings_by_owner_name(owner_name):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under user with name {}".format(owner_name))
        cursor.execute("SELECT l.listing_name, u.name AS user_name, l.description, l.listed_date, "
                       "tag.name AS tag_name, l.owner_id FROM listing l "
                       "LEFT JOIN listing_tag lt ON l.listing_name = lt.listing_name AND l.owner_id = lt.owner_id  "
                       "LEFT JOIN tag AS tag ON lt.tag_id = tag.tag_id "
                       "LEFT JOIN users AS u ON l.owner_id = u.id "
                       "WHERE l.owner_id IN (SELECT u2.id FROM users u2 "
                       "WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(username) LIKE LOWER(%s)) "
                       "GROUP BY l.listing_name, u.name, l.description, l.listed_date, tag.name, l.owner_id "
                       "ORDER BY listed_date DESC;",
                       (owner_name, owner_name,))
        return cursor.fetchall()


# for search queries by all kinds of entries
def get_listings_by_all(all_entries):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting listings under all entries with query {}".format(all_entries))
        cursor.execute("SELECT l.listing_name, u.name AS user_name, l.description, l.listed_date, "
                       "tag.name AS tag_name, l.owner_id FROM listing l "
                       "LEFT JOIN listing_tag lt ON l.listing_name = lt.listing_name AND l.owner_id = lt.owner_id "
                       "LEFT JOIN tag AS tag ON lt.tag_id = tag.tag_id "
                       "LEFT JOIN users AS u ON l.owner_id = u.id "
                       "WHERE l.owner_id IN (SELECT u2.id FROM users u2 WHERE LOWER(name) "
                       "LIKE LOWER(%s) OR LOWER(username) LIKE LOWER(%s)) "
                       "OR l.listing_name IN (SELECT lt2.listing_name FROM listing_tag lt2 "
                       "WHERE tag_id IN (SELECT tag2.tag_id FROM tag tag2 WHERE LOWER(name) LIKE LOWER(%s))) "
                       "AND l.owner_id IN (SELECT lt2.owner_id FROM listing_tag lt2 "
                       "WHERE tag_id IN (SELECT tag2.tag_id FROM tag tag2 WHERE LOWER(name) LIKE LOWER(%s))) "
                       "OR LOWER(l.listing_name) LIKE LOWER(%s) "
                       "GROUP BY l.listing_name, u.name, l.description, l.listed_date, tag.name, l.owner_id "
                       "ORDER BY listed_date DESC;",
                       (all_entries, all_entries, all_entries, all_entries, all_entries,))
        return cursor.fetchall()


def get_popular_listings():
    with DatabaseCursor() as cursor:
        cursor.execute('''select l.listing_name, l.owner_id, count(*)
                          from listing l, bid b
                          where l.listing_name = b.listing_name and l.owner_id = b.owner_id and l.is_available = 'true'
                          group by l.listing_name, l.owner_id
                          order by count(*) desc
                          limit 5''')
        return cursor.fetchall()


def get_expensive_listings():
    with DatabaseCursor() as cursor:
        cursor.execute('''select l.listing_name, l.owner_id , max(price)
                          from listing l , bid b 
                          where l.listing_name = b.listing_name and l.owner_id = b.owner_id and l.is_available = 'true'
                          group by l.listing_name, l.owner_id
                          order by max(price) desc
                          limit 5''')
        return cursor.fetchall()


def get_listings_with_tags(owner_id):
    with DatabaseCursor() as cursor:
        cursor.execute('''select l.listing_name, l.owner_id, l.description, lt.tag_id, tag.name AS tag_name,
                        l.is_available, l.listed_date from listing l inner join listing_tag lt on l.listing_name = lt.listing_name
                        and l.owner_id = lt.owner_id inner join tag tag on lt.tag_id = tag.tag_id 
                        and l.owner_id = %s''', (owner_id,))
        return cursor.fetchall()