from db import tag_queries


class ListingTag:

    def __init__(self, tag_id, listing_name, owner_id):
        self.tag_id = tag_id
        self.listing_name = listing_name
        self.owner_id = owner_id

    def insert_listing_tag(self):
        """
        Creates a new listing tag
        :return: True or false to indicate if the insertion failed
        """
        return tag_queries.insert_listing_tag(self.tag_id, self.listing_name, self.owner_id)





