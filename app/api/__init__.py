from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api', __name__)


from app.api import auth, projects, users
