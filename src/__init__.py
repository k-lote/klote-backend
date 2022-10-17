from flask import Flask, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import dotenv
import os
from .helpers.generateCarne import gerarPDF

dotenv.load_dotenv(dotenv.find_dotenv())

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)
app.config.from_object('config')

def create_app():
    from .routes.allotment import allotment
    from .routes.user import auth
    from .routes.lot import lot
    from .routes.customer import customer
    from .routes.finances import finances

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
    app.register_blueprint(finances, url_prefix="/finances")
   
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")
        return "API is running", 200

    @app.route("/pdf/<name>")
    def pdfCreate(name):
        file = gerarPDF(name, 100)
        #with open('arquivopdf.pdf', 'rb') as static_file:
        return send_file(file, download_name=f"{name}.pdf", as_attachment=True)

    return app