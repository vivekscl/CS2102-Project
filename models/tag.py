from db import tag_queries


class Tag:

    def __init__(self, tag_id, name):
        self.tag_id = tag_id
        self.name = name

    def create_tag(self):
        """
        Creates a new listing
        :return: True or false to indicate if the insertion failed
        """
        return tag_queries.insert_tag(self.name)

    def update_tag(self, name=None):
        """
        All params default to None first. In the method they are given the values of the object. If a value is given,
        then only that value is updated while the rest remains the same
        :return: True or False to indicate if the update failed
        """
        name = name if name is not None else self.name
        return tag_queries.update_tag(self.tag_id, name)

def get_all_tags():
    rows = tag_queries.get_all_tags()
    if rows is None:
        return None
    return [Tag(**row) for row in rows]

