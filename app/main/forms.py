from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    is_active = BooleanField()
    description = TextAreaField('Description', validators=[DataRequired()])
    tags_list = StringField('Tags', validators=[])
    skills_list = StringField('Skills', validators=[])
    submit = SubmitField('Submit')

    def tags(self):
        return [tag.strip() for tag in self.tags_list.data.split(",")]

    def skills(self):
        return [skill.strip() for skill in self.skills_list.data.split(",")]

    def populate(self, project):
        if project.name:
            self.name.data = project.name
        if project.name:
            self.is_active.data = project.is_active
        if project.name:
            self.description.data = project.description
        if project.name:
            self.skills_list.data = ",".join(skill.name for skill in project.skills)
        if project.name:
            self.tags_list.data = ",".join(tag.name for tag in project.tags)


class EditUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    major = StringField('Major', validators=[Length(min=0, max=64), DataRequired()])
    about = TextAreaField('About me', validators=[Length(min=0, max=1024)])
    interests = TextAreaField('Interests', validators=[Length(min=0, max=140)])
    skills_list = StringField('Skills (comma separated)', validators=[])
    submit = SubmitField('Submit')

    def populate(self, user):
        if user.firstname:
            self.firstname.data = user.firstname
        if user.lastname:
            self.lastname.data = user.lastname
        if user.major:
            self.major.data = user.major
        if user.about:
            self.about.data = user.about
        if user.interests:
            self.interests.data = user.interests
        if user.skills:
            self.skills_list.data = ",".join(skill.name for skill in user.skills)

    def skills(self):
        return [skill.strip() for skill in self.skills_list.data.split(",")]


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)