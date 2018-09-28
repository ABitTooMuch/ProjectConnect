from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

contributions = db.Table('contributors',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('contributor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    projects_involved = db.relationship('Project', secondary=contributions, lazy='dynamic',
                                        backref=db.backref('contributors', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # hashes and salts
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def join_project(self, project):
        if not self.is_contributor(project):
            self.projects_involved.append(project)

    def leave_project(self, project):
        if self.is_contributor(project):
            self.projects_involved.append(project)

    def is_contributor(self, project):
        return self.projects_involved.filter(
            contributions.c.contributor_id == project.id).count() > 0


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    status = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
