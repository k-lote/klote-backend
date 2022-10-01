from datetime import datetime
from email.policy import default
from .. import db
from .. import ma

class Lot(db.Model):
    allotment_id = db.Column(db.Integer, db.ForeignKey('allotment.id'), primary_key=True, nullable=False)
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    block = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, allotment_id, number, block, value, is_available=True):
        self.allotment_id = allotment_id
        self.number = number
        self.block = block
        self.value = value
        self.is_available = is_available

class LotSchema(ma.Schema):
    class Meta:
        fields = ('allotment_id', 'number', 'block', 'value', 'is_available')

lot_history_id_seq = db.Sequence('lot_history_id_seq')

class LotHistory(db.Model):
    __tablename__ = 'lot_history'
    id = db.Column(db.Integer, lot_history_id_seq ,primary_key=True, nullable=False)
    allotment_id = db.Column(db.Integer, db.ForeignKey('lot.allotment_id'), nullable=False)
    number = db.Column(db.Integer, db.ForeignKey('lot.number') , nullable=False)
    description = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, allotment_id, number, description):
        self.allotment_id = allotment_id
        self.number = number
        self.description = description
    
class Lot_historySchema(ma.Schema):
    class Meta:
        fields = ('id', 'allotment_id', 'number', 'description', 'created_at')

lot_history_schema = Lot_historySchema()
lots_history_schema = Lot_historySchema(many=True)
lot_schema = LotSchema()
lots_schema = LotSchema(many=True)