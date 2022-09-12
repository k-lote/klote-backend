from datetime import datetime
from .. import db,ma

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