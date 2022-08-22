from flask import Blueprint, request
from .models import User
from .__init__ import db

auth = Blueprint("auth", __name__)

@auth.route("/")
def login():
    return "ok"

@auth.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")
    first_login = True

    user = User.query.filter_by(email=email).first()

    if user:
        return "User already exists", 400
    
    new_user = User(email, password, name, cpf, phone, first_login)
    db.session.add(new_user)
    db.session.commit()

    return "User created", 201