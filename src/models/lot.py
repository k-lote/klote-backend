from datetime import datetime
from .. import db
from .. import ma

class Lot(db.Model):
    allotment_id = db.Column(db.Integer, db.ForeignKey('allotment.id'), primary_key=True, nullable=False)
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    block = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, allotment_id, number, block, value):
        self.allotment_id = allotment_id
        self.number = number
        self.block = block
        self.value = value

class LotSchema(ma.Schema):
    class Meta:
        fields = ('allotment_id', 'number', 'block', 'value')

lot_schema = LotSchema()
lots_schema = LotSchema(many=True)