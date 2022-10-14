from flask import Blueprint, request, jsonify 
from ..models.finances import Installment, installment_schema, installments_schema
from .. import db

finances = Blueprint('finances', __name__)

# Installment
@finances.route('/installment/register', methods=['POST'])
def register_installment():
    value = request.json.get('value')
    date = request.json.get('date')
    is_paid = request.json.get('is_paid')
    installment_number = request.json.get('installment_number')
    allottment_id = request.json.get('allottment_id')
    number = request.json.get('number')


    try:
        installment = Installment(value, date, installment_number, allottment_id, number, is_paid)
        db.session.add(installment)
        db.session.commit()
        return installment_schema.jsonify(installment), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500

@finances.route('/installment/get_installment/<int:id>', methods=['GET'])
def get_installment(id):
    installment = Installment.query.filter_by(cod=id).first()

    if not installment:
        return jsonify({'message': 'Installment not found'}), 404

    return installment_schema.jsonify(installment), 200

@finances.route('/installment/get_installments', methods=['GET'])
def get_installments():
    installments = Installment.query.all()

    if not installments:
        return jsonify({'message': 'Installments not found'}), 404

    return installments_schema.jsonify(installments), 200

@finances.route('/installment/update/<int:id>', methods=['PUT'])
def update_installment(id):
    is_paid = request.json.get('is_paid')

    installment = Installment.query.filter_by(cod=id).first()

    if not installment:
        return jsonify({'message': 'Installment not found'}), 404

    try:
        installment.is_paid = is_paid

        db.session.commit()
        return installment_schema.jsonify(installment), 200
    except:
        return jsonify({'message': 'An error occurred'}), 500

@finances.route('/installment/delete/<int:id>', methods=['DELETE'])
def delete_installment(id):
    installment = Installment.query.filter_by(cod=id).first()

    if not installment:
        return jsonify({'message': 'Installment not found'}), 404

    try:
        db.session.delete(installment)
        db.session.commit()
        return jsonify({'message': 'Installment deleted successfully'}), 200
    except:
        return jsonify({'message': 'An error occurred'}), 500

# Purcharse
'''
@finances.route('/purcharse/register', methods=['POST'])
def register_purcharse():
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')
    customer_id = request.json.get('customer_id')
    date_purcharse = request.json.get('date_purcharse')

    try:
        purcharse = Purcharse(allotment_id, number, customer_id, date_purcharse)
        db.session.add(purcharse)
        db.session.commit()
        return purcharse_schema.jsonify(purcharse), 200
    except:
        return jsonify({'message': 'An error occurred'}), 500
    
@finances.route('/purcharse/get_purcharse/<int:id>', methods=['GET'])
def get_purcharse(id):
    purcharse = Purcharse.query.filter_by(id=id).first()

    if not purcharse:
        return jsonify({'message': 'Purcharse not found'}), 404

    return purcharse_schema.jsonify(purcharse), 200

@finances.route('/purcharse/get_purcharse', methods=['GET'])
def get_purcharse():
    purcharse = Purcharse.query.all()

    if not purcharse:
        return jsonify({'message': 'Purcharse not found'}), 404

    return purcharse_schemas.jsonify(purcharse), 200

@finances.route('/purcharse/update/<int:id>', methods=['PUT'])
def update_purcharse(id):
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')
    customer_id = request.json.get('customer_id')
    date_purcharse = request.json.get('date_purcharse')

    purcharse = Purcharse.query.filter_by(id=id).first()

    if not purcharse:
        return jsonify({'message': 'Purcharse not found'}), 404

    try:
        purcharse.allotment_id = allotment_id
        purcharse.number = number
        purcharse.customer_id = customer_id
        purcharse.date_purcharse = date_purcharse

        db.session.commit()
        return purcharse_schema.jsonify(purcharse), 200
    except:
        return jsonify({'message': 'An error occurred'}), 500

@finances.route('/purcharse/delete/<int:id>', methods=['DELETE'])
def delete_purcharse(id):
    purcharse = Purcharse.query.filter_by(id=id).first()

    if not purcharse:
        return jsonify({'message': 'Purcharse not found'}), 404

    try:
        db.session.delete(purcharse)
        db.session.commit()
        return jsonify({'message': 'Purcharse deleted successfully'}), 200
    except:
        return jsonify({'message': 'An error occurred'}), 500
'''