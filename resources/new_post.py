from flask_restful import Resource
from common.db_models import db, Posts, Comments
from common.db_schemas import post_schema, comment_schema
from common.util import validate_commit, validate_request


class Post(Resource):
    def get(self, id):
        pass
