from database import Database
import uuid
import datetime

class Project:

    collection = 'projects'

    def __init__(self, name, description, status,
                 creation_time=datetime.datetime.utcnow(), project_id=None):
        self._id = uuid.uuid4() if uuid is None else project_id
        self.creation_time = creation_time
        self.name = name
        self.description = description
        self.status = status

    def save_to_db(self):
        Database.insert(Project.collection, self.to_json())

    @classmethod
    def from_db(cls, _id):
        data = Database.find_one({_id: _id})
        return cls(**data)

    def to_json(self):
        return {
            "_id": self.project_id,
            "name": self.name,
            "creation_time": self.creation_time,
            "status": self.status,
            "description": self.description
        }

