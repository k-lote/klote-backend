from datetime import datetime
from .. import db, ma

installment_cod_seq = db.Sequence('installment_cod_seq', metadata=db.MetaData())

class Installment(db.Model):
    cod = db.Column(db.Integer, installment_cod_seq, primary_key=True, unique=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    installment_number = db.Column(db.Integer, nullable=False)
    allotment_id = db.Column(db.Integer, db.ForeignKey('lot.allotment_id'), nullable=False)
    lot_number = db.Column(db.Integer, db.ForeignKey('lot.number'), nullable=False)

    def __init__(self, value, date, installment_number, allotment_id, lot_number, is_paid = False):
        self.value = value
        self.date = date
        self.is_paid = is_paid
        self.installment_number = installment_number
        self.allotment_id = allotment_id
        self.lot_number = lot_number
    
class InstallmentSchema(ma.Schema):
    class Meta:
        fields = ('cod', 'value', 'date', 'is_paid', 'installment_number', 'allotment_id', 'lot_number')
    
installment_schema = InstallmentSchema()
installments_schema = InstallmentSchema(many=True)
