from db import DatabaseCursor
from flask import current_app
import psycopg2


def get_loans_under_bidder(bidder_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting bid with bid ID {} from database".format(bidder_id))
        cursor.execute('select * from loan where bidder_id = %s;', (bidder_id,))
        return cursor.fetchall()


def insert_loan(bidder_id, listing_id, bid_date, borrow_date, return_date, return_loc, pickup_loc):
    try:
        with DatabaseCursor() as cursor:
            cursor.execute('INSERT INTO loan VALUES(%s, %s, %s, %s, %s, %s, %s);', (bidder_id, listing_id, bid_date,
                                                                                    borrow_date, return_date,
                                                                                    return_loc, pickup_loc))
            current_app.logger.info("Loan added to database: [{}, {}, {}, {}, {}, {}, {}]"
                                    .format(bidder_id, listing_id, bid_date, borrow_date, return_date, return_loc,
                                            pickup_loc))
            return True
    except psycopg2.IntegrityError:
        current_app.logger.error("INSERTION FAILED: [{}, {}, {}, {}, {}, {}, {}]"
                                 .format(bidder_id, listing_id, bid_date, borrow_date, return_date, return_loc,
                                         pickup_loc))
        return False


def get_loan_of_listing(listing_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Getting loan with listing ID {} from database".format(listing_id))
        cursor.execute('select * from loan where listing_id = %s;', (listing_id,))
        return cursor.fetchone()


def delete_loan_of_listing(listing_id):
    with DatabaseCursor() as cursor:
        current_app.logger.info("Deleting loan with listing ID {} from database"
                                .format(listing_id))
        cursor.execute("delete from loan where listing_id = %s", (listing_id,))
