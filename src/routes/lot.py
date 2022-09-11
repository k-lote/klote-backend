from flask import Blueprint, request, jsonify 
from ..models.lot import Lot, lot_schema
from .. import db
from .. import ma

lot = Blueprint('lot', __name__)

@lot.route('/register', methods=['POST'])
def register():
    block = request.json.get('block')
    value = request.json.get('value')
    
    new_lot = Lot(block, value)
    db.session.add(new_lot)
    db.session.commit()
    return 'Allotment created', 201

@lot.route('/get_lot/<int:allotment_id>', methods=['GET'])
def get_lot(number):
    lot = Lot.query.filter_by(number=number).first()

    if not lot:
        return 'Lot not found', 400

    return jsonify({'number': lot.number, 'block': lot.block, 'value': lot.value}), 200

@lot.route('/update/<number>', methods=['PUT'])
def update(number):
    block = request.json.get('block')
    value = request.json.get('value')

    lot = Lot.query.filter_by(number=number).first()

    if not lot:
        return jsonify({"message": "Lot not found", "data": {}}), 404
    try:
        if block != None: lot.block = block
        if value != None: lot.value = value


        db.session.commit()
        result = lot_schema.dump(lot)
        return jsonify({"message": "Lot updated", "data": result}), 200
    except:
        return jsonify({"message": "Error updating lot", "data": {}}), 500 

@lot.route('/delete/<number>', methods=['DELETE'])
def delete(number):
    lot = Lot.query.filter_by(number=number).first()

    if not lot:
        return jsonify({"message": "Lot not found", "data": {}}), 404

    try:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message": "Lot deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting lot", "data": {}}), 500