from flask import Blueprint, request, jsonify 
from ..models.allotment import Allotment, allotment_schema, allotments_schema
from ..models.user import User_klote
from ..models.allotment_access import Allotment_access, allotment_access_schema, allotments_access_schema
from .. import db

allotment = Blueprint('allotment', __name__)

@allotment.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    cep = request.json.get('cep')
    address = request.json.get('address')
    img_url = request.json.get('img_url') or None
    logo_url = request.json.get('logo_url') or None
    users_access = request.json.get('users_access') or None
    
    try:
        new_allotment = Allotment(name, cep, address, img_url, logo_url)
        db.session.add(new_allotment)
        db.session.commit()
        result = allotment_schema.dump(new_allotment)
        for user_id in users_access:
            user = User_klote.query.filter_by(user_id=user_id).first()
    
            if not user:
                return f"User {user_id} not found", 400

            try:
                allotment_id = result['id']
                new_access = Allotment_access(user_id, allotment_id)
                db.session.add(new_access)
                db.session.commit()
            except Exception as e:
                print(e)
                return "Error creating access", 500

        return jsonify({'message': 'Allotment created', 'data': result}), 201
    except Exception as e:
        print(e)
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
    allotment = Allotment.query.filter_by(id=id).first()

    if not allotment:
        return jsonify({"message": "Allotment not found", "data": {}}), 404

    try:
        db.session.delete(allotment)
        db.session.commit()
        allotment_access = Allotment_access.query.filter_by(allotment_id=id).all()
        for access in allotment_access:
            db.session.delete(access)
            db.session.commit()

        return jsonify({"message": "Allotment deleted", "data": {}}), 200
    except:
        return jsonify({"message": "Error deleting allotment", "data": {}}), 500