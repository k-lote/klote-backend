from flask import Blueprint, request, jsonify 
from ..models.customer import Customer
from .. import db

client = Blueprint('client', __name__)

@client.route('/register', methods=['POST'])
def register():
    endereco = request.json.get('endereco')
    status = request.json.get('status')
    telefone1 = request.json.get('telefone1')
    telefone2 = request.json.get('telefone2')
    cpf = request.json.get('cpf')
    nome = request.json.get('nome')
    cnpj = request.json.get('cnpj')
    razao_social = request.json.get('razao_social')
    email = request.json.get('email')

    new_client = Customer(endereco, status, telefone1, telefone2, cpf, nome, cnpj, razao_social, email)
    db.session.add(new_client)
    db.session.commit()

    return 'Client created', 201

@client.route('/get_client', methods=['POST'])
def get_client():
    client_id = request.json.get('client_id')

    client = Customer.query.filter_by(id_cliente=client_id).first()

    if not client:
        return 'Client not found', 404

    return jsonify({'id_cliente': client.id_cliente, 'endereco': client.endereco, 'status': client.status, 'telefone1': client.telefone1, 'telefone2': client.telefone2, 'cpf': client.cpf, 'nome': client.nome, 'cnpj': client.cnpj, 'razao_social': client.razao_social, 'email': client.email}), 200

