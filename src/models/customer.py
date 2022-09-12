from datetime import datetime
from .. import db, ma

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    address = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    phone1 = db.Column(db.String(20), nullable=False)
    phone2 = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    corporate_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, address, status, phone1, phone2, cpf, name, cnpj, corporate_name):
        self.address = address
        self.status = status
        self.phone1 = phone1
        self.phone2 = phone2
        self.cpf = cpf
        self.name = name
        self.cnpj = cnpj
        self.corporate_name = corporate_name

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'status', 'phone1', 'phone2', 'cpf', 'name', 'cnpj', 'corporate_name')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)