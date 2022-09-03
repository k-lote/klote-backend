import datetime
import jwt
from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps
from ..models.user import User_klote
from .. import app

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = User_klote.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'message': 'user not found"'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])
        return jsonify({'message': 'Login successful', 'token': token.decode('UTF-8'), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)})
    return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': []}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User_klote.query.filter_by(email=auth.username).first()
        except:
            return jsonify({'message': 'token is invalid or expired', 'data': []}), 401
        return f(current_user, *args, **kwargs)
    return decorated