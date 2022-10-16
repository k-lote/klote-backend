from datetime import datetime
from .. import db, ma

customer_id_seq = db.Sequence('customer_id_seq', metadata=db.MetaData())

class Customer(db.Model):
    id = db.Column(db.Integer, customer_id_seq, primary_key=True, unique=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user_klote.user_id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    phone1 = db.Column(db.String(20), nullable=False)
    phone2 = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    corporate_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, admin_id, address, phone1, phone2, cpf, name, cnpj, corporate_name, email, is_active=True):
        self.admin_id = admin_id
        self.address = address
        self.is_active = is_active
        self.phone1 = phone1
        self.phone2 = phone2
        self.cpf = cpf
        self.name = name
        self.cnpj = cnpj
        self.corporate_name = corporate_name
        self.email = email

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'status', 'phone1', 'phone2', 'cpf', 'name', 'cnpj', 'corporate_name', 'email')

class CustomerHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    costumer_id = db.Column(db.Integer, db.ForeignKey('costumer.id'), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, costumer_id, description):
        self.costumer_id = costumer_id
        self.description = description
    
class CustomerHistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'costumer_id', 'description')

class Purchase(db.Model):
    allotment_id = db.Column(db.Integer, db.ForeignKey('lot.allotment_id'), primary_key=True, nullable=False)
    lot_number = db.Column(db.Integer, db.ForeignKey('lot.number'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_purchase = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, allotment_id, lot_number, customer_id, date_purchase = None):
        self.allotment_id = allotment_id
        self.lot_number = lot_number
        self.customer_id = customer_id
        if date_purchase is not None: self.date_purchase = date_purchase

class PurchaseSchema(ma.Schema):
    class Meta:
        fields = ('allotment_id', 'number', 'customer_id', 'date_purchase')
    
purchase_schema = PurchaseSchema()
purchase_schemas = PurchaseSchema(many=True)
customer_history_schema = CustomerHistorySchema()
customers_history_schema = CustomerHistorySchema(many=True)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)