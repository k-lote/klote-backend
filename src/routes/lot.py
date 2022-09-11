from flask import Blueprint, request, jsonify 
from ..models.lot import Lot, lot_schema
from ..models.allotment import Allotment
from .. import db
from .. import ma

lot = Blueprint('lot', __name__)

@lot.route('/register', methods=['POST'])
def register():
    allotment_id = request.json.get('allotment_id')
    block = request.json.get('block')
    value = request.json.get('value')

    allotment = Allotment.query.filter_by(id=allotment_id).first()    

    if not allotment:
        return 'Allotment not found', 404
    
    last_number = Lot.query.filter_by(allotment_id=allotment_id).order_by(Lot.number.desc()).first()

    if not last_number:
        number = 1
    else:
        last_number = last_number.number
        number = last_number + 1
    try:
        new_lot = Lot(allotment_id, number, block, value)
        db.session.add(new_lot)
        db.session.commit()

        return jsonify({'message': 'Lot created successfully', 'data': lot_schema.dump(new_lot)}), 201
    except:
        return 'An error ocurred creating the lot', 500

@lot.route('/get_lot/<int:allotment_id>', methods=['GET'])
def get_lot(number):
    lot = Lot.query.filter_by(number=number).first()

    if not lot:
        return 'Lot not found', 400

    return jsonify({'number': lot.number, 'block': lot.block, 'value': lot.value}), 200

@lot.route('/get_lots/<int:allotment_id>', methods=['GET'])
def get_lots(allotment_id):
    lots = Lot.query.filter_by(allotment_id=allotment_id).all()

    if not lots:
        return 'Lots not found', 400

    return jsonify({'lots': lot_schema.dump(lots, many=True)}), 200

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

@lot.route('/delete/', methods=['DELETE'])
def delete(number):
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')
    lot = Lot.query.filter_by(allotment_id=allotment_id, number=number).first()

    if not lot:
        return jsonify({"message": "Lot not found", "data": {}}), 404

    try:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message": "Lot deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting lot", "data": {}}), 500