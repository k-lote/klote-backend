from flask import Blueprint, request, jsonify

from src.models.allotment import Allotment 
from ..models.customer import Customer, customer_schema, customers_schema, CustomerHistory, customer_history_schema, customers_history_schema, Purchase, purchase_schema, purchase_schemas
from ..models.user import User_klote
from ..models.lot import Lot
from .. import db
import datetime

customer = Blueprint('client', __name__)

@customer.route('/register', methods=['POST'])
def register():
    address = request.json.get('address')
    phone1 = request.json.get('phone1')
    phone2 = request.json.get('phone2') or None
    cpf = request.json.get('cpf') or None
    name = request.json.get('name')
    cnpj = request.json.get('cnpj') or None
    corporate_name = request.json.get('corporate_name') or None
    admin_id = request.json.get('admin_id')
    email = request.json.get('email')
    lots = request.json.get('lots') or []

    if not address or not phone1 or not name or not admin_id or not email:
        return jsonify({'msg': 'Missing arguments'}), 400

    try:
        new_customer = Customer(admin_id, address, phone1, phone2, cpf, name, cnpj, corporate_name, email)
        admin = User_klote.query.filter_by(user_id=admin_id).first()
        
        for lot in lots:
            lot_disponibility = Lot.query.filter_by(allotment_id=lot['allotment_id'], number=lot['number']).first()
            if lot_disponibility.is_available:
                new_purchase = Purchase(lot['allotment_id'], lot['number'], new_customer.id)
                db.session.add(new_purchase)
                db.session.commit()
                lot_disponibility.is_available = False
                db.session.commit()
            else:
                return jsonify({'msg': 'Lot is not available'}), 400
        
        if admin:
            db.session.add(new_customer)
            db.session.commit()

        return jsonify({'message': 'Customer created successfully', 'data': customer_schema.dump(new_customer)}), 201
    except Exception as e:
        print(e)
        return 'An error ocurred creating the customer', 500

@customer.route('/get_customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.filter_by(id=id).first()
    purchases_query = Purchase.query.all()
    allotments_query = Allotment.query.all()
    lots_query = Lot.query.all()

    if not customer:
        return 'Customer not found', 400

    customer = customer_schema.dump(customer)
    try:
        customer["lots"] = []

        purchases = [purchase for purchase in purchases_query if purchase.customer_id == customer["id"]]
        #purchases = Purchase.query.filter_by(customer_id=customer["id"]).all()
        for purchase in purchases:
            allotment = [allotment for allotment in allotments_query if allotment.id == purchase.allotment_id][0]
            #allotment = Allotment.query.filter_by(id=purchase.allotment_id).first()
            lot = [lot for lot in lots_query if lot.allotment_id == allotment.id and lot.number == purchase.lot_number][0]
            #lot = Lot.query.filter_by(allotment_id=purchase.allotment_id, number=purchase.lot_number).first()
            customer["lots"].append({
                "allotment_id": allotment.id,
                "allotment_name": allotment.name,
                "lot_number": lot.number,
                "block": lot.block
            })
    except Exception as e:
        print(e)
        return 'An error ocurred getting the customer', 500

    return jsonify({'customer': customer}), 200

@customer.route('/get_customers/<int:admin_id>', methods=['GET'])
def get_customers_by_admin(admin_id):
    customers = Customer.query.filter_by(admin_id=admin_id).all()
    purchases_query = Purchase.query.all()
    allotments_query = Allotment.query.all()
    lots_query = Lot.query.all()

    if not customers:
        return 'Customers not found', 400
    
    response = customers_schema.dump(customers)

    for customer in response:
        customer["lots"] = []

        purchases = [purchase for purchase in purchases_query if purchase.customer_id == customer["id"]]
        #purchases = Purchase.query.filter_by(customer_id=customer["id"]).all()
        for purchase in purchases:
            allotment = [allotment for allotment in allotments_query if allotment.id == purchase.allotment_id][0]
            #allotment = Allotment.query.filter_by(id=purchase.allotment_id).first()
            lot = [lot for lot in lots_query if lot.allotment_id == allotment.id and lot.number == purchase.lot_number][0]
            #lot = Lot.query.filter_by(allotment_id=purchase.allotment_id, number=purchase.lot_number).first()
            customer["lots"].append({
                "allotment_id": allotment.id,
                "allotment_name": allotment.name,
                "lot_number": lot.number,
                "block": lot.block
            })

    return jsonify({'data': response}), 200

@customer.route('/get_customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    purchases_query = Purchase.query.all()
    allotments_query = Allotment.query.all()
    lots_query = Lot.query.all()

    if not customers:
        return 'Customers not found', 400
    
    response = customers_schema.dump(customers)

    for customer in response:
        customer["lots"] = []

        purchases = [purchase for purchase in purchases_query if purchase.customer_id == customer["id"]]
        #purchases = Purchase.query.filter_by(customer_id=customer["id"]).all()
        for purchase in purchases:
            allotment = [allotment for allotment in allotments_query if allotment.id == purchase.allotment_id][0]
            #allotment = Allotment.query.filter_by(id=purchase.allotment_id).first()
            lot = [lot for lot in lots_query if lot.allotment_id == allotment.id and lot.number == purchase.lot_number][0]
            #lot = Lot.query.filter_by(allotment_id=purchase.allotment_id, number=purchase.lot_number).first()
            customer["lots"].append({
                "allotment_id": allotment.id,
                "allotment_name": allotment.name,
                "lot_number": lot.number,
                "block": lot.block
            })

    return jsonify({'data': response}), 200

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
        purchases = Purchase.query.filter_by(customer_id=id).all()
        
        if purchases:
            for purchase in purchases:
                lot = Lot.query.filter_by(allotment_id=purchase.allotment_id, number = purchase.lot_number).first()
                lot.is_available = True

                db.session.commit()

        db.session.delete(customer)
        db.session.commit()

        return jsonify({'message': 'Customer deleted successfully', 'data': customer_schema.dump(customer)}), 200
    except Exception as e:
        print(e)
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

# CUSTOMER PURCHASE
@customer.route('/purchase/register', methods=['POST'])
def register_purchase():
    customer_id = request.json.get('customer_id')
    lot_number = request.json.get('lot_number')
    allotment_id = request.json.get('allotment_id')
    date = request.json.get('date') or None

    try:
        new_customer_purchase = Purchase(allotment_id, lot_number, customer_id, date)

        try:
            lot = Lot.query.filter_by(allotment_id=allotment_id, number=lot_number).first()

            if not lot:
                return jsonify({"message": "Lot not found", "data": {}}), 404
            
            if lot.is_available == False:
                return jsonify({"message": "Lot is not available", "data": {}}), 404

            lot.is_available = False
            db.session.commit()
        except:
            return 'An error ocurred updating the lot', 500

        db.session.add(new_customer_purchase)
        db.session.commit()

        return jsonify({'message': 'Customer purchase created successfully', 'data': purchase_schema.dump(new_customer_purchase)}), 201
    except:
        return 'An error ocurred creating the customer purchase', 500

@customer.route('/purchase/get_customer_purchase/<int:id>', methods=['GET'])
def get_customer_purchase(id):
    customer_purchase = Purchase.query.filter_by(customer_id=id).first()

    if not customer_purchase:
        return 'Customer purchase not found', 400

    return jsonify({'customer_purchase': purchase_schemas.dump(customer_purchase)}), 200

@customer.route('/purchase/get_customers_purchases', methods=['GET'])
def get_customers_purchases():
    customers_purchases = Purchase.query.all()

    if not customers_purchases:
        return 'Customers purchases not found', 400

    return jsonify({'customers_purchases': purchase_schemas.dump(customers_purchases)}), 200

@customer.route('/purchase/delete', methods=['DELETE'])
def delete_purchase():
    allotment_id = request.json.get('allotment_id')
    lot_number = request.json.get('lot_number')
    customer_id = request.json.get('customer_id')
    
    customer_purchase = Purchase.query.filter_by(allotment_id=allotment_id, lot_number=lot_number, customer_id=customer_id).first()

    if not customer_purchase:
        return jsonify({"message": "Customer purchase not found", "data": {}}), 404

    try:
        try:
            lot = Lot.query.filter_by(allotment_id=allotment_id, number=lot_number).first()
            
            if not lot:
                return jsonify({"message": "Lot not found", "data": {}}), 404

            lot.is_available = True
            db.session.commit()
        except:
            return 'An error ocurred updating the lot', 500

        db.session.delete(customer_purchase)
        db.session.commit()

        return jsonify({'message': 'Customer purchase deleted successfully', 'data': purchase_schema.dump(customer_purchase)}), 200
    except:
        return 'An error ocurred deleting the customer purchase', 500