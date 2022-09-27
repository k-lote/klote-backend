from datetime import datetime
from .. import db, ma

customer_id_seq = db.Sequence('customer_id_seq', metadata=db.MetaData())

class Customer(db.Model):
    id = db.Column(db.Integer, customer_id_seq, primary_key=True, unique=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user_klote.user_id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    phone1 = db.Column(db.String(20), nullable=False)
    phone2 = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    corporate_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, admin_id, address, status, phone1, phone2, cpf, name, cnpj, corporate_name, email):
        self.admin_id = admin_id
        self.address = address
        self.status = status
        self.phone1 = phone1
        self.phone2 = phone2
        self.cpf = cpf
        self.name = name
        self.cnpj = cnpj
        self.corporate_name = corporate_name
        self.email = email

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'status', 'phone1', 'phone2', 'cpf', 'name', 'cnpj', 'corporate_name')

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

customer_history_schema = CustomerHistorySchema()
customers_history_schema = CustomerHistorySchema(many=True)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)