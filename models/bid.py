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

    def update_bid(self, listing_id=None, bid_date=None, price=None):
        """
        All params default to None first. In the method they are given the values of the object. If a value is given,
        then only that value is updated while the rest remains the same
        :return: True or False to indicate if the update failed
        """
        listing_id = listing_id if listing_id is not None else self.listing_id
        bid_date = bid_date if bid_date is not None else self.bid_date
        price = price if price is not None else self.price
        return bid_queries.update_bid(self.bidder_id, listing_id, bid_date, price)


def get_bids_under_bidder(bidder_id):
    rows = bid_queries.get_bids_under_bidder(bidder_id)
    return dict_list_to_bid_list(rows)


def get_bids_under_listing(listing_id):
    rows = bid_queries.get_bids_under_listing(listing_id)
    return dict_list_to_bid_list(rows)


def get_bid_under_listing_and_bidder(bidder_id, listing_id):
    row = bid_queries.get_bid_under_listing_and_bidder(bidder_id, listing_id)
    if row is None:
        return None
    return Bid(**row)


def dict_list_to_bid_list(rows):
    if rows is None:
        return None
    return [Bid(**row) for row in rows]


def delete_all_bids_of_listing_not_under_bidder(listing_id, bidder_id):
    bid_queries.delete_all_bids_of_listing_not_under_bidder(listing_id, bidder_id)


def delete_bids_of_listing(listing_id):
    bid_queries.delete_bids_of_listing(listing_id)
