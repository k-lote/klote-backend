from crypt import methods
from flask import Blueprint, request, jsonify 
from ..models.lot import Lot, lot_schema, lots_schema, LotHistory, lot_history_schema, lots_history_schema
from ..models.allotment import Allotment
from ..models.customer import Purchase, Customer, customer_schema
from ..models.finances import Installment, installment_schema, installments_schema
from .. import db
from .. import ma

lot = Blueprint('lot', __name__)

@lot.route('/register', methods=['POST'])
def register():
    allotment_id = request.json.get('allotment_id')
    block = request.json.get('block')
    value = request.json.get('value')
    is_available = request.json.get('is_available') or True

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
        new_lot = Lot(allotment_id, number, block, value, is_available)
        db.session.add(new_lot)
        db.session.commit()

        return jsonify({'message': 'Lot created successfully', 'data': lot_schema.dump(new_lot)}), 201
    except Exception as e:
        print(e)
        return 'An error ocurred creating the lot', 500

@lot.route('/get_lot', methods=['POST'])
def get_lot():
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')

    try:
        lot = Lot.query.filter_by(allotment_id=allotment_id, number=number).first()
        if not lot:
            return 'Lot not found', 400

        result = lot_schema.dump(lot)
        result['history'] = {}
        lot_history = LotHistory.query.filter_by(allotment_id=allotment_id, number=number).all()
        lot_history_dump = lots_history_schema.dump(lot_history)
        for history in lot_history_dump:
            result['history'][history['id']] = history

        if lot.is_available == False:
            customer_purchase = Purchase.query.filter_by(allotment_id=allotment_id, lot_number=number).first()
            customer = Customer.query.filter_by(id=customer_purchase.customer_id).first()
            result['customer'] = customer_schema.dump(customer)

       
            finances = Installment.query.filter_by(allotment_id=allotment_id, lot_number=number).all()
            finances_dump = installments_schema.dump(finances)
            result['installments'] = []
            
            for finance in finances_dump:
                result['installments'].append(finance)
                
       
        

        return jsonify({"data": result, "message": "Lot found"}), 200
    except Exception as e:
        print(e)
        return 'An error ocurred getting the lot', 500

@lot.route('/get_lots', methods=['GET'])
def get_all_lots():
    lots = Lot.query.all()

    if not lots:
        return 'Lots not found', 400

    return jsonify({'data': lots_schema.dump(lots)}), 200

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

#LOT HISTORY
@lot.route('/history/register', methods=['POST'])
def history_register():
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')
    description = request.json.get('description')
    
    lot = Lot.query.filter_by(allotment_id=allotment_id, number=number).first()

    if not lot:
        return 'Lot not found', 400

    try:
        new_lot_history = LotHistory(allotment_id, number, description)
        db.session.add(new_lot_history)
        db.session.commit()

        return jsonify({'message': 'Lot history created successfully', 'data': lot_history_schema.dump(new_lot_history)}), 201
    except:
        return 'An error ocurred creating the lot history', 500

@lot.route('/history/get_lot_history/', methods=['GET'])
def get_lot_history():
    allotment_id = request.json.get('allotment_id')
    number = request.json.get('number')
    lot_history = LotHistory.query.filter_by(allotment_id=allotment_id, number=number).all()

    if not lot_history:
        return 'Lot history not found', 400

    return jsonify({'lot_history': lots_history_schema.dump(lot_history, many=True)}), 200

@lot.route('/history/update/<int:id>', methods=['PUT'])
def history_update(id):
    description = request.json.get('description')

    lot_history = LotHistory.query.filter_by(id=id).first()

    if not lot_history:
        return jsonify({"message": "Lot history not found", "data": {}}), 404
    try:
        if description != None: lot_history.description = description

        db.session.commit()
        result = lot_history_schema.dump(lot_history)
        return jsonify({"message": "Lot history updated", "data": result}), 200
    except:
        return jsonify({"message": "Error updating lot history", "data": {}}), 500

@lot.route('/history/delete/', methods=['DELETE'])
def history_delete(id):
    id = request.json.get('id')
    lot_history = LotHistory.query.filter_by(id=id).first()

    if not lot_history:
        return jsonify({"message": "Lot history not found", "data": {}}), 404

    try:
        db.session.delete(lot_history)
        db.session.commit()
        return jsonify({"message": "Lot history deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting lot history", "data": {}}), 500