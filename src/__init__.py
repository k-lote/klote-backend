from turtle import title
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_pydantic_spec import FlaskPydanticSpec
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)
app.config.from_object('config')

spec = FlaskPydanticSpec('flask',title='Documentação API - Klote')
spec.register(app)

def create_app():
    from .routes.allotment import allotment
    from .routes.user import auth
    from .routes.lot import lot
    from .routes.customer import customer

    dotenv.load_dotenv(dotenv.find_dotenv())
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(auth, url_prefix="/user")
    app.register_blueprint(allotment, url_prefix="/allotment")
    app.register_blueprint(lot, url_prefix="/lot")
    app.register_blueprint(customer, url_prefix="/customer")

    
   
    @app.route("/", methods=["GET"])
    def index():
        return "API is running", 200

    

    return app