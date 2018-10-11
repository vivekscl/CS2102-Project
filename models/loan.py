from db import loan_queries


class Loan:

    def __init__(self, bidder_id, listing_id, bid_date, borrow_date, return_date, return_loc, pickup_loc):
        self.bidder_id = bidder_id
        self.listing_id = listing_id
        self.bid_date = bid_date
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.return_loc = return_loc
        self.pickup_loc = pickup_loc

    def create_loan(self):
        """
        Creates a new loan
        :return: True or False to indicate if the insertion failed
        """
        return loan_queries.insert_loan(self.bidder_id, self.listing_id, self.bid_date, self.borrow_date,
                                        self.return_date, self.return_loc, self.pickup_loc)


def get_loans_under_bidder(bidder_id):
    rows = loan_queries.get_loans_under_bidder(bidder_id)
    if rows is None:
        return None
    return [Loan(**row) for row in rows]

