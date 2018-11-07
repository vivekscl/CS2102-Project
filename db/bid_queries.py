from db import DatabaseCursor
from flask import current_app
import psycopg2


def get_bids_under_bidder(bidder_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with bid ID {} from database".format(bidder_id))
        cursor.execute('select * from bid where bidder_id = %s;', (bidder_id,))
        return cursor.fetchall()


def get_bids_under_listing(listing_name, owner_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with listing {} of owner {} from database".format(listing_name, owner_id))
        cursor.execute('select * from bid where listing_name = %s and owner_id = %s;', (listing_name, owner_id))
        return cursor.fetchall()


def get_bid_under_listing_and_bidder(bidder_id, listing_name, owner_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with listing {}, owner {} and bidder {} from database"
                                .format(listing_name, owner_id, bidder_id))
        cursor.execute('select * from bid where listing_name = %s and owner_id = %s and bidder_id = %s;',
                       (listing_name, owner_id, bidder_id))
        return cursor.fetchone()


def insert_bid(bidder_id, listing_name, owner_id, bid_date, price):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO bid VALUES(%s, %s, %s, %s, %s);', (bidder_id, listing_name, owner_id, bid_date,
                                                                           price))
            current_app.logger.info("Bid added to database: [{}, {}, {}, {}, {}]"
                                    .format(bidder_id, listing_name, owner_id, bid_date, price))

            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}, {}, {}, {}, {}]".format(bidder_id, listing_name, owner_id,
                                                                                 bid_date, price))
        return False
    except psycopg2.InternalError as e:
        current_app.logger.error("INSERTION FAILED: [{}, {}, {}, {}, {}]".format(bidder_id, listing_name, owner_id,
                                                                                 bid_date, price))
        return False


def update_bid(bidder_id, listing_name, owner_id, bid_date, price):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('UPDATE bid SET price = %s '
                           'where bidder_id = %s and listing_name = %s and owner_id = %s and bid_date = %s;',
                           (price, bidder_id, listing_name, owner_id, bid_date))
            current_app.logger.info("Bid {} updated: [{}, {}, {}, {}]"
                                    .format(bidder_id, listing_name, owner_id, bid_date, price))
            return True
    except psycopg2.Error:
        current_app.logger.error("UPDATE FAILED: [{}, {}, {}, {}, {}]".format(bidder_id, listing_name, owner_id,
                                                                              bid_date, price))
        return False

