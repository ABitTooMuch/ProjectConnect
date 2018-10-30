from app import db

contributions = db.Table('contributors',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('contributor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)
project_likes = db.Table('project_likes',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
project_requests = db.Table('project_requests',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    @classmethod
    def find(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def exists(cls, name):
        return cls.query.filter_by(name=name).count() > 0

    def __repr__(self):
        return '<Tag %s>' % self.name

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    @classmethod
    def find(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def exists(cls, name):
        return cls.query.filter_by(name=name).count() > 0

    def __repr__(self):
        return '<Skill %s>' % self.name


