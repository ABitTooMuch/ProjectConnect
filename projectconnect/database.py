import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():

        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['test']

    @staticmethod
    def insert(collection, data):
        result = Database.DATABASE[collection].insert_one(data)
        print(result.inserted_id)
        print(Database.DATABASE[collection].find_one(data))

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)