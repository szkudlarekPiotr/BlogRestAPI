from flask_restful import Resource, abort, request
from common.db_models import db, Users
from common.db_schemas import user_schema
from common.util import validate_request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token


class Login(Resource):
    def post(self):
        args = validate_request(user_schema, request, partial=True)
        user = db.session.execute(
            db.select(Users).where(Users.email == args["email"])
        ).scalar()
        if not user:
            abort(400, message="User not found")
        if not check_password_hash(user.password, args["password"]):
            abort(400, message="Wrong password")
        else:
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(user)
            return {"accesss": access_token, "refresh": refresh_token}
