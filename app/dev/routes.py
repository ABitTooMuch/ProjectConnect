from flask import url_for, flash, render_template, request, current_app
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect


from app import db
from app.dev import bp
from app.dev.forms import LoginForm, RegistrationForm, ProjectForm
from app.models.project import Project
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

    return render_template('dev/user_login.html', title='Sign In', form=form)


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
    return render_template('dev/user_registration.html', title='Register', form=form)


@bp.route('/')
@bp.route('/explore')
@bp.route('/index')
def explore():
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('dev.explore', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('dev.explore', page=projects.prev_num) if projects.has_prev else None
    print(projects.has_next)
    print(next_url)
    return render_template('dev/explore.html', title='Explore', projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/my_projects')
@login_required
def my_projects():
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = current_user.projects.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('dev.my_projects', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('dev.my_projects', page=projects.prev_num) if projects.has_prev else None
    return render_template('dev/user_projects.html', title='My Projects', projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@ bp.route('/new_project', methods=['GET', 'POST'])
@ login_required
def new_project():
    form = ProjectForm()
    # if the form has valid form data
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data)

        db.session.add(project)
        current_user.join_project(project)
        db.session.commit()

        return redirect(url_for('dev.my_projects'))

    return render_template('dev/project_create.html', title='New Project', form=form)


@bp.route('/project/<project_id>')
def project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    return render_template('dev/project.html', title=project.name, project=project)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = user.projects.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('dev.user', username=username, page=projects.next_num) if projects.has_next else None
    prev_url = url_for('dev.user', username=username, page=projects.prev_num) if projects.has_prev else None
    return render_template('dev/user.html', title=username, user=user, projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/like/<project_id>')
@login_required
def like_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    current_user.like_project(project)
    db.session.commit()
    return redirect(url_for('dev.project', project_id=project.id))


@bp.route('/unlike/<project_id>')
@login_required
def unlike_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    current_user.unlike_project(project)
    db.session.commit()
    return redirect(url_for('dev.project', project_id=project.id))
