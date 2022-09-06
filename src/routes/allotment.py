from flask import Blueprint, request, jsonify 
from ..models.allotment import Allotment

allotment = Blueprint('allotment', __name__)

@allotment.route('/register', methods=['POST'])
def register():
    pass

@allotment.route('/get_allotment', methods=['POST'])
def get_allotment():
    pass

@allotment.route('/update', methods=['PUT'])
def update():
    pass

@allotment.route('/delete', methods=['DELETE'])
def delete():
    pass