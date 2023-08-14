from flask_restful import Resource
from common.db_models import db, Posts
from common.db_schemas import post_schema


class HomePage(Resource):
    def get(self):
        posts = db.session.execute(db.select(Posts)).scalars()
        results = [post_schema.dump(item) for item in posts]
        return {"data": results}
