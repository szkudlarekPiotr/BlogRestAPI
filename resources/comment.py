from flask_restful import Resource, request
from common.db_models import Comments, db
from common.db_schemas import comment_schema
from common.util import validate_commit, validate_request
from flask_jwt_extended import jwt_required, get_jwt_identity


class AddComment(Resource):
    @jwt_required()
    def post(self, post_id):
        args = validate_request(comment_schema, request)
        new_comment = Comments(
            body=args["body"], post_id=post_id, user_id=get_jwt_identity()
        )
        db.session.add(new_comment)
        validate_commit()
        return {"comment": comment_schema.dump(new_comment)}
