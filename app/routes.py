from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

from app import app, db
from flask import render_template, flash, url_for
from app.forms import LoginForm, RegistrationForm, ProjectForm
from app.models.project import Project
from app.models.user import User


@app.route('/')
@app.route('/explore')
@app.route('/index')
def explore():
    return render_template('dev/explore.html', title='Explore')


@app.route('/my_projects')
@login_required
def my_projects():
    return render_template('dev/user_projects.html', title='My Projects')


@ app.route('/new_project', methods=['GET', 'POST'])
@ login_required
def new_project():

    form = ProjectForm()
    # if the form if the request has valid form data
    if form.validate_on_submit():
        project = Project(name=form.name.data, description = form.description.data)

        db.session.add(project)
        current_user.join_project(project)
        db.session.commit()

        return redirect(url_for('my_projects'))

    return render_template('dev/project_create.html', title='New Project', form=form)


@app.route('/project/<project_name>')
def project(project_name):
    project = Project.query.filter_by(name=project_name).first_or_404()
    return render_template('dev/project.html', title=project_name, project=project)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('dev/user.html', title='', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in they will be redirected
    if current_user.is_authenticated:
        return redirect(url_for('explore'))
    form = LoginForm()
    # if the form if the request has valid form data
    if form.validate_on_submit():
        # find user
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # redirect the user to a different page after login
        return redirect(url_for('explore'))

    return render_template('dev/user_login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('explore'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Already Registered.")
        return redirect(url_for('explore'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successful Registration!")
        return redirect(url_for('login'))
    return render_template('dev/user_registration.html', title='Register', form=form)