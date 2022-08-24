from flask import Blueprint, request
from ..models.user import User_klote
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

auth = Blueprint("auth", __name__)

@auth.route("/")
def login():
    return "ok"

@auth.route("/register", methods=["POST"])
def register():
    # Get data from json request
    user_id = request.json.get("user_id")
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")

    check_email = User_klote.query.filter_by(email=email).first()
    check_cpf = User_klote.query.filter_by(cpf=cpf).first()
    check_phone = User_klote.query.filter_by(phone=phone).first()

    # validations
    if check_email:
        return "Email already registered", 400
    if check_cpf:
        return "CPF already registered", 400
    if check_phone:
        return "Phone already registered", 400
    if User_klote.validates_password(password)[0] is False:
        return User_klote.validates_password(password)[1], 400
    if User_klote.validates_email(email)[0] is False:
        return User_klote.validates_email(email)[1], 400
    if User_klote.validates_cpf(cpf)[0] is False:
        return User_klote.validates_cpf(cpf)[1], 400
    if User_klote.validates_phone(phone)[0] is False:
        return User_klote.validates_phone(phone)[1], 400
    if User_klote.validates_name(name)[0] is False:
        return User_klote.validates_name(name)[1], 400
    
    new_user = User_klote(user_id, email, generate_password_hash(password, method='sha256'), name, cpf, phone)
    db.session.add(new_user)
    db.session.commit()


    return "User created", 201

@auth.route("/delete", methods=["DELETE"])
def delete():
    user_id = request.json.get("user_id")
    user = User_klote.query.filter_by(user_id=user_id).first()

    if not user:
        return "User not found", 400

    db.session.delete(user)
    db.session.commit()

    return "User deleted", 200

@auth.route("/update", methods=["PUT"])
def update():
    user_id = request.json.get("user_id")
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")
    first_login = True

    user = User_klote.query.filter_by(user_id=user_id).first()

    if not user:
        return "User not found", 400

    if User_klote.validates_password(password)[0] is False:
        return User_klote.validates_password(password)[1], 400
    if User_klote.validates_email(email)[0] is False:
        return User_klote.validates_email(email)[1], 400
    if User_klote.validates_cpf(cpf)[0] is False:
        return User_klote.validates_cpf(cpf)[1], 400
    if User_klote.validates_phone(phone)[0] is False:
        return User_klote.validates_phone(phone)[1], 400
    if User_klote.validates_name(name)[0] is False:
        return User_klote.validates_name(name)[1], 400
    
    user.email = email
    user.password = generate_password_hash(password, method='sha256')
    user.name = name
    user.cpf = cpf
    user.phone = phone
    user.first_login = first_login
    db.session.commit()

    return "User updated", 200

@auth.route("/reset_password", methods=["PUT"])
def reset_password():
    user_id = request.json.get("user_id")
    password = request.json.get("password")

    user = User_klote.query.filter_by(user_id=user_id).first()

    if not user:
        return "User not found", 400

    if User_klote.validates_password(password)[0] is False:
        return User_klote.validates_password(password)[1], 400
    
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()

    return "User updated", 200