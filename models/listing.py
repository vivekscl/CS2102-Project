from db import listing_queries
from db import tag_queries, DatabaseCursor

class Listing:

    def __init__(self, listing_id, owner_id, name, description, is_available=True):
        self.listing_id = listing_id
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.is_available = is_available

    def create_listing(self):
        """
        Creates a new listing
        :return: True or false to indicate if the insertion failed
        """
        return listing_queries.insert_listing(self.owner_id, self.name, self.description, self.is_available)

    def update_listing(self, owner_id=None, name=None, description=None, is_available=None):
        """
        All params default to None first. In the method they are given the values of the object. If a value is given,
        then only that value is updated while the rest remains the same
        :return: True or False to indicate if the update failed
        """
        owner_id = owner_id if owner_id is not None else self.owner_id
        name = name if name is not None else self.name
        description = description if description is not None else self.description
        is_available = is_available if is_available is not None else self.is_available
        return listing_queries.update_listing(self.listing_id, owner_id, name, description, is_available)


def get_listing_by_id(listing_id):
    row = listing_queries.get_listing_by_id(listing_id)
    if row is None:
        return None
    return Listing(**row)


def get_listings_under_owner(owner_id):
    rows = listing_queries.get_listings_under_owner(owner_id)
    if rows is None:
        return None
    return [Listing(**row) for row in rows]

def get_all_listings():
    with DatabaseCursor() as cursor:
        cursor.execute('''select * 
                          from listing''')
        result = cursor.fetchall()
    return result

def get_listings_owner_id():
    with DatabaseCursor() as cursor:
        cursor.execute('''select * 
                          from listing l 
                          order by l.owner_id''')
        result=cursor.fetchall()
    return result

number = 5

# extract top 'number' listings if there exists
def get_expensive_listings():
    with DatabaseCursor() as cursor:
        cursor.execute('''select l.listing_id, l.name, l.is_available , max(price)
                          from listing l , bid b 
                          where l.listing_id = b.listing_id
                          group by l.listing_id, l.name, l.is_available
                          order by max(price) desc''')
        result = cursor.fetchall()
        if len(result)<= number:
            return result
        else:
            return result[0:number]

# extract top 'number' listings if there exists
def get_popular_listings():
    with DatabaseCursor() as cursor:
        cursor.execute('''select l.listing_id, l.name, l.is_available, count(*)
                          from listing l, bid b
                          where l.listing_id = b.listing_id
                          group by l.listing_id, l.name, l.is_available
                          order by count(*) desc''')
        result = cursor.fetchall()
        if len(result)<=number:
            return result
        else:
            return result[0:number]

def get_all_listing():
    rows = listing_queries.get_all_listing()
    if rows is None:
        return None
    return [Listing(**row) for row in rows]


def get_listings_by_owner_name(owner_name):
    rows = listing_queries.get_listings_by_owner_name(owner_name)
    if rows is None:
        return None
    return [Listing(**row) for row in rows]


def get_listings_by_tag_name(tag_name):
    rows = tag_queries.get_listings_by_tag_name(tag_name)
    if rows is None:
        return None
    return [Listing(**row) for row in rows]
