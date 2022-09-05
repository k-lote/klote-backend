from flask import Blueprint, request, jsonify 
from ..models.loteamento import Loteamento

loteamento = Blueprint('loteamento', __name__)

@loteamento.route('/register', methods=['POST'])
def register():
    pass

@loteamento.route('/get_loteamento', methods=['POST'])
def get_loteamento():
    pass

@loteamento.route('/get_loteamentos/<int:user_id>', methods=['GET'])
def get_loteamentos(user_id):
    pass

@loteamento.route('/update', methods=['PUT'])
def update():
    pass

@loteamento.route('/delete', methods=['DELETE'])
def delete():
    pass