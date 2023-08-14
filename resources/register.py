from flask_restful import Resource, abort, request
from common.db_models import db, Users
from common.db_schemas import user_schema
from common.util import validate_commit, validate_request, existing_user
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token


class Register(Resource):
    def post(self):
        args = validate_request(user_schema, request)
        new_user = Users(
            name=args["name"],
            email=args["email"],
            password=generate_password_hash(args["password"], salt_length=10),
        )
        if existing_user(args["email"]):
            abort(401, message="User already exists")
        db.session.add(new_user)
        validate_commit()
        new_user = db.session.execute(
            db.select(Users).where(Users.email == args["email"])
        ).scalar()
        access_token = create_access_token(new_user)
        refresh_token = create_refresh_token(new_user)
        return {"access": access_token, "refresh": refresh_token}
