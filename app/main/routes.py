from datetime import datetime

from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app import db
from flask import render_template, url_for, request, current_app, g

from app.main import bp
from app.main.forms import ProjectForm, SearchForm, EditUserForm
from app.models.attributes import Tag, Skill
from app.models.project import Project
from app.models.user import User


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.search_form = SearchForm()


@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def explore():
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('main.explore', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('main.explore', page=projects.prev_num) if projects.has_prev else None
    print(projects.has_next)
    print(next_url)
    return render_template('explore.html', title='Explore', projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/my_projects')
@login_required
def my_projects():
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = current_user.projects.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('main.my_projects', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('main.my_projects', page=projects.prev_num) if projects.has_prev else None
    return render_template('user_projects.html', title='My Projects', projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    # if the form has valid form data
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          is_active=form.is_active.data
                          )
        db.session.add(project)
        current_user.join_project(project)
        for t in form.tags():
            tag = Tag.find(t)
            if tag:
                if not project.has_tag(tag):
                    project.add_tag(tag)
            else:
                tag = Tag(t)
                db.session.add(tag)
                project.add_tag(tag)

        db.session.commit()

        return redirect(url_for('main.my_projects'))

    return render_template('project_create.html', title='New Project', form=form)


@bp.route('/project/<project_id>')
def project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    return render_template('project.html', title=project.name, project=project)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = user.projects.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('main.user', username=username, page=projects.next_num) if projects.has_next else None
    prev_url = url_for('main.user', username=username, page=projects.prev_num) if projects.has_prev else None
    return render_template('user.html', title=username, user=user, projects=projects.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/like/<project_id>')
@login_required
def like_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    current_user.like_project(project)
    db.session.commit()
    return redirect(url_for('main.project', project_id=project.id))


@bp.route('/unlike/<project_id>')
@login_required
def unlike_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    current_user.unlike_project(project)
    db.session.commit()
    return redirect(url_for('main.project', project_id=project.id))


@bp.route('/search')
def search():
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects, total = Project.search(g.search_form.q.data, page_no, items_per_page)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page_no + 1) \
        if total > page_no * items_per_page else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page_no - 1) \
        if page_no > 1 else None
    return render_template('search.html', title='Search', projects=projects,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    form.populate(current_user)
    # if the form has valid form data
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.major = form.major.data
        current_user.about = form.about.data
        current_user.interests = form.interests.data

        for s in form.skills():
            skill = Skill.find(s)
            if skill:
                if not current_user.has_skill(skill):
                    current_user.add_skill(skill)
            else:
                skill = Skill(s)
                db.session.add(skill)
                current_user.add_skill(skill)

        current_user.last_update = datetime.utcnow()

        db.session.commit()

        return redirect(url_for('main.user', username=current_user.username))

    return render_template('user_edit.html', title='Edit Profile', form=form)


@bp.route('/edit_project/<project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    form = ProjectForm()
    project = Project.query.filter_by(id=project_id).first()
    form.populate(project)
    # if the form has valid form data
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.active = form.is_active.data

        for t in form.tags():
            tag = Tag.find(t)
            if tag:
                if not project.has_tag(tag):
                    project.add_tag(tag)
                    db.session.commit()
            else:
                tag = Tag(t)
                db.session.add(tag)
                project.add_tag(tag)
                db.session.commit()

        project.last_update = datetime.utcnow()

        db.session.commit()

        return redirect(url_for('main.my_projects'))

    return render_template('project_edit.html', title='Edit Project', form=form)


@bp.route('/delete_project/<project_id>', methods=['GET'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.my_projects'))


@bp.route('/user2/<username>')
@login_required
def user2(username):
    user = User.query.filter_by(username=username).first_or_404()
    items_per_page = request.args.get('items_per_page', current_app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    page_no = request.args.get('page', 1, type=int)
    projects = user.projects.order_by(Project.last_update.desc()).paginate(page_no, items_per_page, False)
    next_url = url_for('main.user', username=username, page=projects.next_num) if projects.has_next else None
    prev_url = url_for('main.user', username=username, page=projects.prev_num) if projects.has_prev else None
    return render_template('user.html', title=username, user=user, projects=projects.items,
                           next_url=next_url, prev_url=prev_url)