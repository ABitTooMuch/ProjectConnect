from flask_restful import Resource, Api
from app.api import bp
from app.models.project import Project
from app.models.user import User
from app import db


class ProjectResource(Resource):
    def get(self, id):
        return {'id': 'Say "Hello, World!"'}

class LikesResource(Resource):
    
    def get(self, project_id, user_id):
        project = Project.query.filter_by(id=project_id).first()
        user = User.query.filter_by(id=user_id).first()
        if not project:
            return {'error': 'project error'}
        if not user:
            return {'error': 'user error'}
        status = True if user.has_liked_project(project) else False

        db.session.commit()
        return {'liked': status}
    
    def post(self, project_id, user_id):
        project = Project.query.filter_by(id=project_id).first()
        user = User.query.filter_by(id=user_id).first()
        user.like_project(project)
        db.session.commit()
        return {'status': 'liked'}

    def delete(self, project_id, user_id):
        project = Project.query.filter_by(id=project_id).first()
        user = User.query.filter_by(id=user_id).first()
        user.unlike_project(project)
        db.session.commit()
        return {'status': 'unliked'}


api = Api(bp)
api.add_resource(ProjectResource, '/project/<int:id>')
api.add_resource(LikesResource, '/project/<int:project_id>/likes/<int:user_id>')
