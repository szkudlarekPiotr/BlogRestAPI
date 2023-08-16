from common.db_models import db, Users
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import abort


def commit():
    try:
        db.session.commit()
        return True
    except SQLAlchemyError:
        abort(500, message=f"Database commit error")


def validate_request(schema, request, **kwargs):
    if not request.is_json:
        args = schema.load(request.args)
    else:
        args = request.get_json(force=True)
    if kwargs.get("partial", False):
        if schema.validate(args, partial=True):
            abort(400, message="Bad request")
        return args
    if schema.validate(args):
        abort(400, message="Missing values")
    return args


def existing_user(email):
    user = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
    if user:
        return True
