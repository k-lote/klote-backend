from unittest import result
from flask import Blueprint, request, jsonify 
from ..models.user import User_klote, user_schema, users_schema
from ..models.allotment import Allotment, allotments_schema
from ..models.allotment_access import Allotment_access
from ..models.lot import Lot, lot_schema, lots_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..helpers.emailSender import send_email_reset_password, send_email_new_guest
import datetime
import jwt
from .. import app
from ..helpers.autentication import token_required, admin_required
from ..helpers.random_password import random_password

auth = Blueprint("auth", __name__) 

@auth.route("/", methods=["GET"])
@token_required
def root(current_user):
    return jsonify({'message': f'Hello {current_user.name}'})

@auth.route("/login", methods=["POST"])
def authenticate():
# login a user
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = User_klote.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'message': 'user not found"'}), 401

    if check_password_hash(user.password, auth.password):
        user_data = user_schema.dump(user)
        token = jwt.encode({"user_data": user_schema.dump(user), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])
        response = jsonify({'message': 'Login successful', 'token': token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 200
        return response
    return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

@auth.route("/register_admin", methods=["POST"])
def register_admin():
# register a new user
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")
    first_login = False
    is_admin = True

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
        new_user = User_klote(email, generate_password_hash(password, method='sha256'), name, cpf, phone, first_login, is_admin)
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
        return jsonify({"message": "User created", "data": result}), 201
    except:
        return jsonify({"message": "Error creating user", "data": {}}), 500

@auth.route("/register_guest", methods=["POST"], strict_slashes=False)
@admin_required
def register_guest():
    email = request.json.get("email")
    password = random_password()
    name = request.json.get("name")
    cpf = request.json.get("cpf")
    phone = request.json.get("phone")
    first_login = True

    # validations
    if User_klote.query.filter_by(email=email).first():
        return "Email already registered", 400
    if User_klote.query.filter_by(cpf=cpf).first():
        return "CPF already registered", 400
    if User_klote.query.filter_by(phone=phone).first():
        return "Phone already registered", 400
    if User_klote.validates_email(email)[0] is False:
        return User_klote.validates_email(email)[1], 400
    if User_klote.validates_cpf(cpf)[0] is False:
        return User_klote.validates_cpf(cpf)[1], 400
    if User_klote.validates_phone(phone)[0] is False:
        return User_klote.validates_phone(phone)[1], 400
    if User_klote.validates_name(name)[0] is False:
        return User_klote.validates_name(name)[1], 400
    
    try:
        new_user = User_klote(email, generate_password_hash(password, method='sha256'), name, cpf, phone, first_login)
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
        send_email_new_guest(email, name, password)
        return jsonify({"message": "Guest created", "data": result}), 201
    except:
        return jsonify({"message": "Error creating user", "data": {}}), 500

@auth.route("/delete/<id>", methods=["DELETE"])
def delete(id):
# delete a user
    user = User_klote.query.filter_by(user_id=id).first()

    if not user:
        return jsonify({"message": "User not found", "data": {}}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting user", "data": {}}), 500

@auth.route("/update/<id>", methods=["PUT"])
def update(id):
# update a user(avaliar quais dados podem ser atualizados)
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
        data = user_schema.dump(user)
        return jsonify({"message": "User updated", "data": data}), 200
    except:
        return jsonify({"message": "Error updating user", "data": {}}), 500

# retorna os dados do usuario a partir do id
@auth.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User_klote.query.filter_by(user_id=user_id).first()

    if not user:
        return "User not found", 400

    data = user_schema.dump(user)

    return jsonify({"message": "User found", "data": data}), 200

# retorna todos os usuarios
@auth.route("/get_users", methods=["GET"])
def get_users():
    try:
        users = User_klote.query.all()
        result = users_schema.dump(users)
        return jsonify({"message": "Users found", "data": result}), 200
    except:
        return jsonify({"message": "Error getting users", "data": {}}), 500

# envia email para resetar a senha
@auth.route("/send_email", methods=["POST"])
def send_email():
    email = request.json.get("email")
    user = User_klote.query.filter_by(email=email).first()

    if not user:
        return "User not found", 404

    send_email_reset_password(user.email, user.name)

    return "Email sent", 200

@auth.route("/add_allotment_access", methods=["POST"])
def add_access():
    user_id = request.json.get("user_id")
    allotment_id = request.json.get("allotment_id")

    user = User_klote.query.filter_by(user_id=user_id).first()
    loteamento = Allotment.query.filter_by(id=allotment_id).first()

    if not user:
        return "User not found", 400
    if not loteamento:
        return "Loteamento not found", 400
    
    try:
        new_access = Allotment_access(user_id, allotment_id)
        db.session.add(new_access)
        db.session.commit()
        return jsonify({"message": "Access added", "data": {}}), 200
    except:
        return jsonify({"message": "Error adding access", "data": {}}), 500

@auth.route('/remove_allotment_access', methods=["DELETE"])
def remove_access():
    user_id = request.json.get("user_id")
    allotment_id = request.json.get("allotment_id")

    user = User_klote.query.filter_by(user_id=user_id).first()
    allotment = Allotment.query.filter_by(id=allotment_id).first()

    if not user:
        return "User not found", 400
    if not allotment:
        return "allotment not found", 400
    
    access = Allotment_access.query.filter_by(user_id=user_id, allotment_id=allotment_id).first()

    if not access:
        return "Access not found", 400

    try:
        db.session.delete(access)
        db.session.commit()
        return jsonify({"message": "Access removed", "data": {}}), 200
    except:
        return jsonify({"message": "Error removing access", "data": {}}), 500

@auth.route('/get_allotments/<int:user_id>', methods=['GET'])
def get_allotments_user(user_id):
    user = User_klote.query.filter_by(user_id=user_id).first()
    if not user:
        return "User not found", 400

    try:
        access = Allotment_access.query.filter_by(user_id=user_id).all()
        allotments = []
        for allotment in access:
            allotment_info = Allotment.query.filter_by(id=allotment.allotment_id).first()
            allotments.append(allotment_info)
        result = allotments_schema.dump(allotments)
        for allotment in result:
            allotment["lots"] = {}
            lots = Lot.query.filter_by(allotment_id=allotment['id']).all()
            lots_data = lots_schema.dump(lots)
            for lot in lots_data:
                allotment['lots'][lot['number']] = lot['status']

        return jsonify({"message": "Allotments found", "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error getting allotments", "data": {}}), 500