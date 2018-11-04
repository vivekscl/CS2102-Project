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


class MostCommonListingTag:
    def __init__(self, tag_name, count):
        self.tag_name = tag_name
        self.count = count


def get_most_common_tag_of_owner(owner_name):
    row = tag_queries.get_most_common_tag_of_owner(owner_name)
    if row is None:
        return None
    return MostCommonListingTag(**row)


def get_tagids_under_listing(listing_name, owner_id):
    rows = tag_queries.get_tagids_under_listing(listing_name, owner_id)
    if rows is None:
        return None
    else:
        result = []
        for row in rows:
            print(row[0])
            result.append(row[0])
    return result


def delete_listing_tags(listing_name, owner_id):
    tag_queries.delete_listing_tags(listing_name, owner_id)
