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
    #app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    ma.init_app(app)

    from .models.user import User_klote
    from .models.user import user_share_schema
    from .models.user import users_share_schema

    from .routes.auth import auth

    app.register_blueprint(auth, url_prefix="/api/user/")

    return app