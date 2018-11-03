from db import listing_queries
from db import tag_queries, DatabaseCursor


class Listing:

    def __init__(self, listing_name, owner_id, description, listed_date, is_available=True):
        self.listing_name = listing_name
        self.owner_id = owner_id
        self.listed_date = listed_date
        self.description = description
        self.is_available = is_available

    def create_listing(self):
        """
        Creates a new listing
        :return: True or false to indicate if the insertion failed
        """
        return listing_queries.insert_listing(self.listing_name, self.owner_id, self.description, self.listed_date,
                                              self.is_available)

    def update_listing(self, listed_date=None, description=None, is_available=None):
        """
        All params default to None first. In the method they are given the values of the object. If a value is given,
        then only that value is updated while the rest remains the same
        :return: True or False to indicate if the update failed
        """
        listed_date = listed_date if listed_date is not None else self.listed_date
        description = description if description is not None else self.description
        is_available = is_available if is_available is not None else self.is_available
        return listing_queries.update_listing(self.listing_name, self.owner_id, description, listed_date, is_available)


def get_listing(listing_name, owner_id):
    row = listing_queries.get_listing(listing_name, owner_id)
    if row is None:
        return None
    return Listing(**row)


def get_listings_under_owner(owner_id):
    rows = listing_queries.get_listings_under_owner(owner_id)
    if rows is None:
        return None
    return [Listing(**row) for row in rows]


def get_all_listing():
    rows = listing_queries.get_all_listing()
    if rows is None:
        return None
    return [Listing(**row) for row in rows]


def get_listings_owner_id():
    with DatabaseCursor() as cursor:
        cursor.execute('''select * 
                          from listing l 
                          order by l.owner_id''')
        result=cursor.fetchall()
    return result


# extract top 'number' listings if there exists
def get_expensive_listings():
    return listing_queries.get_expensive_listings()


# extract top 'number' listings if there exists
def get_popular_listings():
    return listing_queries.get_popular_listings()


# Custom class for inner join query to return listing with tag name
class ListingWithTagName:
    def __init__(self, listing_name, owner_id, description, tag_id, tag_name, is_available, listed_date):
        self.listing_name = listing_name
        self.owner_id = owner_id
        self.description = description
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.is_available = is_available
        self.listed_date = listed_date


# get listings together with tag name
def get_listings_with_tags(owner_id):
    rows = listing_queries.get_listings_with_tags(owner_id)
    if rows is None:
        return None
    return [ListingWithTagName(**row) for row in rows]


class ListingForSearch:
    def __init__(self, listing_name, user_name, description, listed_date, tag_name, owner_id):
        self.listing_name = listing_name
        self.owner_id = owner_id
        self.description = description
        self.tag_name = tag_name
        self.listed_date = listed_date
        self.user_name = user_name

    def __eq__(self, other):
        return self.listing_name == other.listing_name and self.owner_id == other.owner_id


# get listings using owner's name
def get_listings_by_owner_name(owner_name):
    rows = listing_queries.get_listings_by_owner_name(owner_name)
    if rows is None:
        return None
    else:
        prev = [ListingForSearch(**row) for row in rows]
        after = []
        for i, elem in enumerate(prev):
            if elem not in after:
                after.append(elem)
            else:
                num = after.index(elem)
                after[num].tag_name += "," + elem.tag_name
        return after


# get listings using tag name
def get_listings_by_tag_name(tag_name):
    rows = listing_queries.get_listings_by_tag_name(tag_name)
    if rows is None:
        return None
    else:
        prev = [ListingForSearch(**row) for row in rows]
        after = []
        for i, elem in enumerate(prev):
            if elem not in after:
                after.append(elem)
            else:
                num = after.index(elem)
                after[num].tag_name += "," + elem.tag_name
        return after


# get listings using listing name
def get_listings_by_listing_name(listing_name):
    rows = listing_queries.get_listings_by_listing_name(listing_name)
    if rows is None:
        return None
    else:
        prev = [ListingForSearch(**row) for row in rows]
        after = []
        for i, elem in enumerate(prev):
            if elem not in after:
                after.append(elem)
            else:
                num = after.index(elem)
                after[num].tag_name += "," + elem.tag_name
        return after
