from flask_restful import Resource, abort
from common.db_models import db, Users, Posts, Comments
from common.db_schemas import post_schema, comment_schema
from common.util import validate_commit, validate_request


class PostInfo(Resource):
    def get(self, post_id):
        post = db.get_or_404(Posts, post_id)
        return post_schema.dump(post)
