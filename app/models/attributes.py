from app import db

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
