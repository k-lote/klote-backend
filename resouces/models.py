from datetime import datetime
from . import db
from . import ma

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,email,password):
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "created_at")

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)
