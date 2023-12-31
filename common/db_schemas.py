from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    is_active = fields.Bool()


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    subtitle = fields.Str(required=True)
    date = fields.Str()
    body = fields.Str(required=True)
    author_name = fields.Str()
    img_url = fields.Str(required=True)
    author_id = fields.Int()


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    body = fields.Str(required=True)
    post_id = fields.Int()
    user_id = fields.Int()


user_schema = UserSchema()
post_schema = PostSchema()
comment_schema = CommentSchema()
