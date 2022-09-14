from datetime import datetime
from .. import db, ma

class Installment(db.Model):
    cod = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')
    installment_number = db.Column(db.Integer, nullable=False)
    allotment_id = db.Column(db.Integer, db.ForeignKey('allotment.id'), nullable=False)
    number = db.Column(db.Integer, db.ForeignKey('lot.number'), nullable=False)

    def __init__(self, value, date, status, installment_number, allotment_id, number):
        self.value = value
        self.date = date
        self.status = status
        self.installment_number = installment_number
        self.allotment_id = allotment_id
        self.number = number
    
class InstallmentSchema(ma.Schema):
    class Meta:
        fields = ('cod', 'value', 'date', 'status', 'installment_number', 'allotment_id', 'number')
    
class Purcharse(db.Model):
    allotment_id = db.Column(db.Integer, db.ForeignKey('lot.allotment_id'), primary_key=True, nullable=False)
    number = db.Column(db.Integer, db.ForeignKey('lot.number'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_purchase = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, allotment_id, number, customer_id, date_purchase):
        self.allotment_id = allotment_id
        self.number = number
        self.customer_id = customer_id
        self.date_purchase = date_purchase

class PurcharseSchema(ma.Schema):
    class Meta:
        fields = ('allotment_id', 'number', 'customer_id', 'date_purchase')
    
purcharse_schema = PurcharseSchema()
purcharse_schemas = PurcharseSchema(many=True)
installment_schema = InstallmentSchema()
installments_schema = InstallmentSchema(many=True)
