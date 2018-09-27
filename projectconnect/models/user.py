from flask import session

from database import Database

class User:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def get_by_email(cls):
        data = Database.find_one("users", {"email": self.email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # check whether a user's password matches the email they sent us
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User does not exist
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # login_valid should have been called
        session['email'] = user_email

    @staticmethod
    def login():
        session['email'] = None

    def get_projects(self):
        pass

    def json(self):
        return {
            "email:": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_db(self):
        Database.insert("users", self.json())