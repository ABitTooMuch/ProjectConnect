from datetime import datetime

from app import db
from app.models.sql.attributes import Tag, Skill

project_tags = db.Table('project_tags',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

project_skills = db.Table('project_skills',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    status = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    tags = db.relationship('Tag', secondary=project_tags, lazy='dynamic',
                           backref=db.backref('projects', lazy='dynamic'))

    skills = db.relationship('Skill', secondary=project_skills, lazy='dynamic',
                           backref=db.backref('projects', lazy='dynamic'))

    def has_tag(self, tag):
        return self.tags.filter(
            project_tags.c.tag_id == tag.id).count() > 0

    def has_tag_name(self, tag_name):
        tag = Tag.find(tag_name)
        return tag and self.has_tag(tag)

    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)

    def has_skill(self, skill):
        return self.skills.filter(
            project_skills.c.skill_id == skill.id).count() > 0

    def has_skill_name(self, skill_name):
        skill = Skill.find(skill_name)
        return skill and self.has_skill(skill)

    def add_skill(self, skill):
        if not self.has_skill(skill):
            self.skills.append(skill)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
