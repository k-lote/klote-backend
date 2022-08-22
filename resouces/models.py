from datetime import datetime
from . import db
from . import ma

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    phone = db.Column(db.String(11), unique=True)
    first_login = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(150), unique=True)

    

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "created_at")

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)
