from flask import Blueprint, request, jsonify 

index = Blueprint("index", __name__)

@index.route("/", methods=["GET"])
def index():
    return "API is running", 200