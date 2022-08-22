from flask import Flask, request, render_template, jsonify, Blueprint, blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    dotenv.load_dotenv(dotenv.find_dotenv())
    app =Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    db.init_app(app)
    ma.init_app(app)

    from .models import User
    from .models import user_share_schema
    from .models import users_share_schema

    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")

    

    return app