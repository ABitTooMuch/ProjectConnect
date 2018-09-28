import unittest

from app import app, db
from app.models.sql.models import User, Project


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_join_project(self):
        user = User(username="dimitri", email="pilodi2@gmail.com")
        project = Project(name="connect")
        db.session.add(user)
        db.session.add(project)
        db.session.commit()
        user.join_project(project)

        self.assertEqual(user.projects_involved.first().name, "connect")
        self.assertEqual(project.contributors.first().username, "dimitri")

if __name__ == '__main__':
    unittest.main(verbosity=2)