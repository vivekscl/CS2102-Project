from flask_login import UserMixin
from db import user_queries
from werkzeug.security import check_password_hash


class User(UserMixin):

    def __init__(self, id, username, name, password_hash, phoneno=None):
        self.id = id
        self.username = username
        self.name = name
        self.password_hash = password_hash
        self.phoneno = phoneno

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_user_info(self):
        """
        This method uses named arguments, all of which are optional. Send in an argument with the keyword name and
        this method will only update that part of the user.
        :return:
        """
    def create_user(self):
        """
        Creates a user by inserting that user into the table using the attributes of the User object
        :return:
        """
        user_queries.insert_user(self.username, self.name, self.password_hash, self.phoneno)


# Keep only update and insert queries inside the User class for the convenience of using the User attributes.
# while other queries are kept outside since you don't require the User attributes for that.
def get_user_by_id(user_id):
    row = user_queries.get_user_by_id(int(user_id))
    if row is None:
        return None
    return User(**row)


def get_user_by_username(username):
    row = user_queries.get_user_by_username(username)
    if row is None:
        return None
    return User(**row)
