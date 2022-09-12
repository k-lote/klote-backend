from datetime import datetime
from .. import db, ma

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