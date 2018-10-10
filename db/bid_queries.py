from db import DatabaseCursor
from flask import current_app
import psycopg2


def get_bids_under_bidder(bidder_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with bid ID {} from database".format(bidder_id))
        cursor.execute('select * from bid where bidder_id = %s;', (bidder_id,))
        return cursor.fetchall()


def get_bids_under_listing(listing_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with listing_id ID {} from database".format(listing_id))
        cursor.execute('select * from bid where listing_id = %s;', (listing_id,))
        return cursor.fetchall()


def insert_bid(bidder_id, listing_id, bid_date, price):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO bid VALUES(%s, %s, %s, %s);', (bidder_id, listing_id, bid_date, price))
            current_app.logger.info("Bid added to database: [{}, {}, {}, {}]"
                                    .format(bidder_id, listing_id, bid_date, price))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}, {}, {}, {}]".format(bidder_id, listing_id, bid_date, price))
        return False
