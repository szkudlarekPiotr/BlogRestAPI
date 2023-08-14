from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from common.db_models import db, Posts, Users
from common.db_schemas import post_schema, comment_schema
from common.util import validate_commit, validate_request
import datetime


class NewPost(Resource):
    @jwt_required()
    def post(self):
        args = validate_request(post_schema, request, partial=True)
        author_id = get_jwt_identity()
        new_post = Posts(
            title=args["title"],
            subtitle=args["subtitle"],
            date=datetime.date.today(),
            body=args["body"],
            author_name=db.session.execute(
                db.Select(Users.name).where(Users.id == author_id)
            ).scalar(),
            img_url=args["img_url"],
            author_id=author_id,
        )
        db.session.add(new_post)
        validate_commit()
        return {"post": post_schema.dump(new_post)}
