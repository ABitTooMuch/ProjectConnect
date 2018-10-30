import unittest

from app import app, db
from app.models.tables import Tag, Skill
from app.models.project import Project
from app.models.user import User

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_join_project(self):
        user1 = User(username="dimitri", email="pilodi2@gmail.com")
        project1 = Project(name="connect")
        db.session.add(user1)
        db.session.add(project1)
        db.session.commit()
        user1.join_project(project1)

        self.assertEqual(user1.projects.first().name, "connect")
        self.assertEqual(project1.contributors.first().username, "dimitri")
        self.assertTrue(user1.is_contributor(project1))

        user2 = User(username="james", email="imabigboy@site.com")
        project2 = Project(name="success")
        db.session.add(user2)
        db.session.add(project2)
        user1.join_project(project2)
        user2.join_project(project1)
        db.session.commit()

        self.assertEqual(2, user1.projects.count())
        self.assertEqual(2, project1.contributors.count())

    def test_user_skills(self):
        user1 = User(username="connect")
        user2 = User(username="success")
        s1 = Skill(name="python")
        s2 = Skill(name="sql")

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        user1.add_skill(s1)
        user2.add_skill(s1)
        user2.add_skill(s2)
        db.session.commit()

        self.assertEqual(1, user1.skills.count())
        self.assertEqual(2, user2.skills.count())
        self.assertTrue(user1.has_skill_name(s1.name))
        self.assertFalse(user1.has_skill_name(s2.name))
        self.assertTrue(Skill.exists(s1.name))

class ProjectModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_project_tags(self):
        project1 = Project(name="connect")
        project2 = Project(name="success")
        tag1 = Tag(name="computer science")
        tag2 = Tag(name="community")

        db.session.add(project1)
        db.session.add(project2)
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()

        project1.add_tag(tag1)
        project2.add_tag(tag1)
        project2.add_tag(tag2)
        db.session.commit()

        self.assertEqual(1, project1.tags.count())
        self.assertEqual(2, project2.tags.count())
        self.assertTrue(project1.has_tag_name(tag1.name))
        self.assertFalse(project1.has_tag_name(tag2.name))
        self.assertTrue(Tag.exists(tag1.name))

    def test_project_skills(self):
        project1 = Project(name="connect")
        project2 = Project(name="success")
        s1 = Skill(name="python")
        s2 = Skill(name="sql")

        db.session.add(project1)
        db.session.add(project2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        project1.add_skill(s1)
        project2.add_skill(s1)
        project2.add_skill(s2)
        db.session.commit()

        self.assertEqual(1, project1.skills.count())
        self.assertEqual(2, project2.skills.count())
        self.assertTrue(project1.has_skill_name(s1.name))
        self.assertFalse(project1.has_skill_name(s2.name))
        self.assertTrue(Skill.exists(s1.name))

    def test_project_likes(self):
        user1 = User(username="dimitri", email="pilodi2@gmail.com")
        user2 = User(username="john", email="john123@gmail.com")
        project1 = Project(name="connect")
        project2 = Project(name="success")
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()

        # test user successfully likes project
        user1.like_project(project1)
        db.session.commit()
        self.assertEqual(True, user1.has_liked_project(project1))

        # test user can't like twice
        user1.like_project(project1)
        db.session.commit()
        self.assertEqual(1, project1.likes())

        # test user can successfully unlike project
        user1.unlike_project(project1)
        db.session.commit()
        self.assertEqual(0, project1.likes())
        self.assertEqual(False, user1.has_liked_project(project1))

        # test multiple users can like the same project
        user1.like_project(project1)
        user2.like_project(project1)
        db.session.commit()
        self.assertEqual(2, project1.likes())

        # test user can like multiple projects
        user1.like_project(project2)
        db.session.commit()
        self.assertEqual(2, user1.projects_liked.count())

if __name__ == '__main__':
    unittest.main(verbosity=2)
