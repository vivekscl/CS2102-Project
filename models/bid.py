from db import bid_queries


class Bid:

    def __init__(self, bidder_id, listing_id, bid_date, price):
        self.bidder_id = bidder_id
        self.listing_id = listing_id
        self.bid_date = bid_date
        self.price = price

    def create_bid(self):
        """
        Creates a new bid
        :return: True or False to indicate if the insertion failed
        """
        return bid_queries.insert_bid(self.bidder_id, self.listing_id, self.bid_date, self.price)


def get_bids_under_bidder(bidder_id):
    rows = bid_queries.get_bids_under_bidder(bidder_id)
    return dict_list_to_bid_list(rows)


def get_bids_under_listing(listing_id):
    rows = bid_queries.get_bids_under_listing(listing_id)
    return dict_list_to_bid_list(rows)


def dict_list_to_bid_list(rows):
    if rows is None:
        return None
    return [Bid(**row) for row in rows]
