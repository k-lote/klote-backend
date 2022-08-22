from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/")
def login():
    return "ok"
