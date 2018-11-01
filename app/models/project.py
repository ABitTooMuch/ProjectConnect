from datetime import datetime

from app import db
from app.models.tables import project_requests, project_tags, project_skills
from app.models.attributes import Tag, Skill


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    status = db.Column(db.String(64))
    creation_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    tags = db.relationship('Tag', secondary=project_tags, lazy='dynamic',
                           backref=db.backref('projects', lazy='dynamic'))

    skills = db.relationship('Skill', secondary=project_skills, lazy='dynamic',
                             backref=db.backref('projects', lazy='dynamic'))

    membership_requests = db.relationship('User', secondary=project_requests, lazy='dynamic',
                                          backref=db.backref('membership_requests', lazy='dynamic'))

    # backrefs:
    #   contributors
    #   liked_by

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

    def likes(self):
        return self.liked_by.count()

    def requests(self):
        return self.membership_requests.all()

    def __repr__(self):
        return '<Post {}>'.format(self.body)
