from flask_restful import Api
from flask import Flask
from common.db_models import db
from common.login_management import jwt
import os
from resources.home import HomePage
from resources.register import Register
from resources.login import Login
from resources.new_post import NewPost
from resources.post import PostInfo

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DB_URI"]
db.init_app(app)
jwt.init_app(app)
api = Api(app)

api.add_resource(HomePage, "/", "/home")
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(NewPost, "/new_post")
api.add_resource(PostInfo, "/post/<int:post_id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
