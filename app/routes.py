from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect

from app import app, db
from flask import render_template, flash, url_for
from app.forms import LoginForm, RegistrationForm
from app.models.user import User

@app.route('/')
@app.route('/explore')
@app.route('/index')
def explore():
    return render_template('explore.html', title='Explore')

@app.route('/projects')
def projects():
    projects = [{"name":"success", "status":"active", "description":"hey, that's pretty  gud"},
                     {"name": "connect", "status": "active", "description": "that's us"}]
    return render_template('projects.html', title='My Projects', projects = projects)

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

    return render_template('login.html', title='Sign In', form=form)

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
    return render_template('register.html', title='Register', form=form)