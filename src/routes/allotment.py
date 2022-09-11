from flask import Blueprint, request, jsonify 
from ..models.allotment import Allotment, allotment_schema, allotments_schema
from .. import db

allotment = Blueprint('allotment', __name__)

@allotment.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    cep = request.json.get('cep')
    address = request.json.get('address')
    img_url = request.json.get('img_url')
    
    try:
        new_allotment = Allotment(name, cep, address, img_url)
        db.session.add(new_allotment)
        db.session.commit()
        result = allotment_schema.dump(new_allotment)
        return jsonify({'message': 'Allotment created', 'data': result}), 201
    except:
        return jsonify({'message': 'Error creating allotment', 'data': {}}), 500

@allotment.route('/get_allotment/<int:allotment_id>', methods=['GET'])
def get_allotment(allotment_id):
    allotment = Allotment.query.filter_by(id=allotment_id).first()

    if not allotment:
        return 'Allotment not found', 400

    return jsonify({'id': allotment.id, 'name': allotment.name, 'cep': allotment.cep, 'address': allotment.address, 'img url':allotment.img_url}), 200

@allotment.route('/get_allotments', methods=['GET'])
def get_allotments():
    try:
        allotments = Allotment.query.all()
        result = allotments_schema.dump(allotments)
        return jsonify({'message': 'Allotments found', 'data': result}), 200
    except:
        return jsonify({'message': 'Error getting allotments', 'data': {}}), 500

@allotment.route('/update/<id>', methods=['PUT'])
def update(id):
    name = request.json.get('name')
    cep = request.json.get('cep')
    address = request.json.get('address')
    img_url = request.json.get('img_url')

    allotment = Allotment.query.filter_by(allotment_id=id).first()

    if not allotment:
        return jsonify({"message": "Allotment not found", "data": {}}), 404
    try:
        if name != None: allotment.name = name
        if cep != None: allotment.cep = cep
        if address != None: allotment.address = address
        if img_url != None: allotment.img_url = img_url

        db.session.commit()
        result = allotment_schema.dump(allotment)
        return jsonify({"message": "Allotment updated", "data": result}), 200
    except:
        return jsonify({"message": "Error updating allotment", "data": {}}), 500 

@allotment.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    allotment = Allotment.query.filter_by(allotment_id=id).first()

    if not allotment:
        return jsonify({"message": "Allotment not found", "data": {}}), 404

    try:
        db.session.delete(allotment)
        db.session.commit()
        return jsonify({"message": "Allotment deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting allotment", "data": {}}), 500