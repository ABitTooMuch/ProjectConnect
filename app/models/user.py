from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.models.attributes import Skill
from app.models.project import Project

contributions = db.Table('contributors',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('contributor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', secondary=contributions, lazy='dynamic',
                               backref=db.backref('contributors', lazy='dynamic'))
    skills = db.relationship('Skill', secondary=user_skills, lazy='dynamic',
                             backref=db.backref('users', lazy='dynamic'))

    def has_skill(self, skill):
        return self.skills.filter(
            user_skills.c.skill_id == skill.id).count() > 0

    def has_skill_name(self, skill_name):
        skill = Skill.find(skill_name)
        return skill and self.has_skill(skill)

    def add_skill(self, skill):
        if not self.has_skill(skill):
            self.skills.append(skill)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # hash and salt password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def join_project(self, project):
        if not self.is_contributor(project):
            self.projects.append(project)

    def leave_project(self, project):
        if self.is_contributor(project):
            self.projects.append(project)

    def is_contributor(self, project):
        return self.projects.filter(
            contributions.c.contributor_id == project.id).count() > 0

@login.user_loader
def load_user(id):
    return User.query.get(int(id))