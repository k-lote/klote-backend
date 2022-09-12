from flask import Blueprint, request, jsonify 
from ..models.customer import Customer, customer_schema, customers_schema, CustomerHistory, customer_history_schema, customers_history_schema
from .. import db

customer = Blueprint('client', __name__)

@customer.route('/register', methods=['POST'])
def register():
    address = request.json.get('address')
    status = request.json.get('status') or 'active'
    phone1 = request.json.get('phone1')
    phone2 = request.json.get('phone2') or None
    cpf = request.json.get('cpf') or None
    name = request.json.get('name')
    cnpj = request.json.get('cnpj') or None
    corporate_name = request.json.get('corporate_name') or None

    try:
        new_customer = Customer(address, status, phone1, phone2, cpf, name, cnpj, corporate_name)
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({'message': 'Customer created successfully', 'data': customer_schema.dump(new_customer)}), 201
    except:
        return 'An error ocurred creating the customer', 500

@customer.route('/get_customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.filter_by(id=id).first()

    if not customer:
        return 'Customer not found', 400

    return jsonify({'customer': customer_schema.dump(customer)}), 200

@customer.route('/get_customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()

    if not customers:
        return 'Customers not found', 400

    return jsonify({'customers': customers_schema.dump(customers)}), 200

@customer.route('/update/<int:id>', methods=['PUT'])
def update(id):
    address = request.json.get('address')
    status = request.json.get('status')
    phone1 = request.json.get('phone1')
    phone2 = request.json.get('phone2') or None
    cpf = request.json.get('cpf') or None
    name = request.json.get('name')
    cnpj = request.json.get('cnpj') or None
    corporate_name = request.json.get('corporate_name') or None

    customer = Customer.query.filter_by(id=id).first()

    if not customer:
        return jsonify({"message": "Customer not found", "data": {}}), 404
    try:
        if address != None: customer.address = address
        if status != None: customer.status = status
        if phone1 != None: customer.phone1 = phone1
        if phone2 != None: customer.phone2 = phone2
        if cpf != None: customer.cpf = cpf
        if name != None: customer.name = name
        if cnpj != None: customer.cnpj = cnpj
        if corporate_name != None: customer.corporate_name = corporate_name

        db.session.commit()

        return jsonify({'message': 'Customer updated successfully', 'data': customer_schema.dump(customer)}), 200
    except:
        return 'An error ocurred updating the customer', 500

@customer.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    customer = Customer.query.filter_by(id=id).first()

    if not customer:
        return jsonify({"message": "Customer not found", "data": {}}), 404

    try:
        db.session.delete(customer)
        db.session.commit()

        return jsonify({'message': 'Customer deleted successfully', 'data': customer_schema.dump(customer)}), 200
    except:
        return 'An error ocurred deleting the customer', 500

# CUSTOMER HISTORY
@customer.route('/history/register', methods=['POST'])
def register_history():
    customer_id = request.json.get('customer_id')
    lot_id = request.json.get('lot_id')
    status = request.json.get('status') or 'active'
    date = request.json.get('date')

    try:
        new_customer_history = CustomerHistory(customer_id, lot_id, status, date)
        db.session.add(new_customer_history)
        db.session.commit()

        return jsonify({'message': 'Customer history created successfully', 'data': customer_history_schema.dump(new_customer_history)}), 201
    except:
        return 'An error ocurred creating the customer history', 500

@customer.route('/history/get_customer_history/<int:id>', methods=['GET'])
def get_customer_history(id):
    customer_history = CustomerHistory.query.filter_by(id=id).first()

    if not customer_history:
        return 'Customer history not found', 400

    return jsonify({'customer_history': customer_history_schema.dump(customer_history)}), 200

@customer.route('/history/get_customers_history', methods=['GET'])
def get_customers_history():
    customers_history = CustomerHistory.query.all()

    if not customers_history:
        return 'Customers history not found', 400

    return jsonify({'customers_history': customers_history_schema.dump(customers_history)}), 200

@customer.route('/history/update/<int:id>', methods=['PUT'])
def update_history(id):
    customer_id = request.json.get('customer_id')
    lot_id = request.json.get('lot_id')
    status = request.json.get('status')
    date = request.json.get('date')

    customer_history = CustomerHistory.query.filter_by(id=id).first()

    if not customer_history:
        return jsonify({"message": "Customer history not found", "data": {}}), 404
    try:
        if customer_id != None: customer_history.customer_id = customer_id
        if lot_id != None: customer_history.lot_id = lot_id
        if status != None: customer_history.status = status
        if date != None: customer_history.date = date

        db.session.commit()

        return jsonify({'message': 'Customer history updated successfully', 'data': customer_history_schema.dump(customer_history)}), 200
    except:
        return 'An error ocurred updating the customer history', 500

@customer.route('/history/delete/<int:id>', methods=['DELETE'])
def delete_history(id):
    customer_history = CustomerHistory.query.filter_by(id=id).first()

    if not customer_history:
        return jsonify({"message": "Customer history not found", "data": {}}), 404

    try:
        db.session.delete(customer_history)
        db.session.commit()

        return jsonify({'message': 'Customer history deleted successfully', 'data': customer_history_schema.dump(customer_history)}), 200
    except:
        return 'An error ocurred deleting the customer history', 500