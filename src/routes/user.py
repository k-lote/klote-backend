from unittest import result
from flask import Blueprint, request, jsonify 
from ..models.user import User_klote, user_schema, users_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..helpers.emailSender import send_email_reset_password
import datetime
import jwt
from .. import app
from ..helpers.autentication import token_required

auth = Blueprint("auth", __name__)
# base route: /api/user/ 

@auth.route("/", methods=["GET"])
@token_required
def root(current_user):
    return jsonify({'message': f'Hello {current_user.name}'})

# registra um novo usuario
@auth.route("/register", methods=["POST"])
def register():
    # Get data from json request
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")

    # validations
    if User_klote.query.filter_by(email=email).first():
        return "Email already registered", 400
    if User_klote.query.filter_by(cpf=cpf).first():
        return "CPF already registered", 400
    if User_klote.query.filter_by(phone=phone).first():
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
    
    try:
        new_user = User_klote(email, generate_password_hash(password, method='sha256'), name, cpf, phone)
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
        return jsonify({"message": "User created", "data": result}), 201
    except:
        return jsonify({"message": "Error creating user", "data": {}}), 500

# login (alterar para retornar o token)
@auth.route("/login", methods=["POST"])
def authenticate():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = User_klote.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'message': 'user not found"'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])
        return jsonify({'message': 'Login successful', 'token': token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)})
    return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

# deleta um usuario
@auth.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    user = User_klote.query.filter_by(user_id=id).first()

    if not user:
        return jsonify({"message": "User not found", "data": {}}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting user", "data": {}}), 500

# atualiza os dados de um usuario (avaliar quais dados podem ser atualizados)
@auth.route("/update/<id>", methods=["PUT"])
def update(id):
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")

    user = User_klote.query.filter_by(user_id=id).first()

    if not user:
        return jsonify({"message": "User not found", "data": {}}), 404
        
    if password != None and User_klote.validates_password(password)[0] is False:
        return User_klote.validates_password(password)[1], 400
    if email != None and User_klote.validates_email(email)[0] is False:
        return User_klote.validates_email(email)[1], 400
    if cpf != None and User_klote.validates_cpf(cpf)[0] is False:
        return User_klote.validates_cpf(cpf)[1], 400
    if phone != None and User_klote.validates_phone(phone)[0] is False:
        return User_klote.validates_phone(phone)[1], 400
    if name != None and User_klote.validates_name(name)[0] is False:
        return User_klote.validates_name(name)[1], 400
    
    try:
        if email != None: user.email = email
        if password != None: user.password = generate_password_hash(password, method='sha256')
        if name != None: user.name = name
        if cpf != None: user.cpf = cpf
        if phone != None: user.phone = phone

        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({"message": "User updated", "data": result}), 200
    except:
        return jsonify({"message": "Error updating user", "data": {}}), 500

# retorna os dados do usuario a partir do id
@auth.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User_klote.query.filter_by(user_id=user_id).first()

    if not user:
        return "User not found", 400

    return jsonify({"user_id": user.user_id, "email": user.email, "name": user.name, "cpf": user.cpf, "phone": user.phone}), 200

# retorna todos os usuarios
@auth.route("/get_users", methods=["GET"])
def get_users():
    users = User_klote.query.all()
    result = users_schema.dump(users)
    return jsonify({"message": "Users found", "data": result}), 200

# envia email para resetar a senha
@auth.route("/send_email", methods=["POST"])
def send_email():
    email = request.json.get("email")
    user = User_klote.query.filter_by(email=email).first()

    if not user:
        return "User not found", 400

    send_email_reset_password(user.email, user.name)

    return "Email sent", 200
