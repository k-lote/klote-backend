from datetime import datetime
from .. import db

class Installment(db.Model):
    cod = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')
    installment_number = db.Column(db.Integer, nullable=False)
    allotment_id = db.Column(db.Integer, db.ForeignKey('allotment.id'), nullable=False)
    number = db.Column(db.Integer, db.ForeignKey('lot.number'), nullable=False)