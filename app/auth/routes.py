from flask import url_for, flash, render_template
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models.user import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in they will be redirected
    if current_user.is_authenticated:
        return redirect(url_for('main.explore'))
    form = LoginForm()
    # if the form if the request has valid form data
    if form.validate_on_submit():
        # find user
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        # redirect the user to a different page after login
        return redirect(url_for('main.explore'))

    return render_template('user_login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.explore'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Already Registered.")
        return redirect(url_for('main.explore'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successful Registration!")
        return redirect(url_for('auth.login'))
    return render_template('user_registration.html', title='Register', form=form)
