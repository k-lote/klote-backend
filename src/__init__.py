from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)
app.config.from_object('config')

def create_app():
    from .routes.user import auth

    dotenv.load_dotenv(dotenv.find_dotenv())
    CORS(app)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(auth, url_prefix="/api/user/")
   
    @app.route("/", methods=["GET"])
    def index():
        return "API is running", 200

    return app