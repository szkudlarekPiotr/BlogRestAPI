from flask_restful import Resource, abort, request
from common.db_models import db, Users, Posts, Comments
from common.db_schemas import post_schema, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from common.util import validate_commit, validate_request


class PostInfo(Resource):
    def get(self, post_id):
        post = db.get_or_404(Posts, post_id)
        post_json = post_schema.dump(post)
        comments = db.session.execute(
            db.select(Comments).where(Comments.post_id == post_id)
        ).scalars()
        comments_list_json = [comment_schema.dump(comment) for comment in comments]
        return {"post": post_json, "comments": comments_list_json}

    @jwt_required()
    def put(self, post_id):
        args = validate_request(post_schema, request)
        post = db.get_or_404(Posts, post_id)
        user = db.get_or_404(Users, get_jwt_identity())
        if not post.author_id == user.id:
            abort(401, message="Only author can edit this post")
        for key in args.keys():
            setattr(post, key, args[key])
        validate_commit()
        return {"data": post_schema.dump(post)}

    @jwt_required()
    def patch(self, post_id):
        args = validate_request(post_schema, request, partial=True)
        post = db.get_or_404(Posts, post_id)
        user = db.get_or_404(Users, get_jwt_identity())
        if not post.author_id == user.id:
            abort(401, message="Only post author can edit this post")
        for key in args.keys():
            setattr(post, key, args[key])
        validate_commit()
        return {"data": post_schema.dump(post)}

    @jwt_required()
    def delete(self, post_id):
        post = db.get_or_404(Posts, post_id)
        db.session.delete(post)
        validate_commit()
        return {"message": "succesfully deleted post"}
