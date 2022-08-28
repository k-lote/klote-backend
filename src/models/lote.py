from datetime import datetime
from .. import db

class Lote(db.Model):
    loteamento_id = db.Column(db.Integer, db.ForeignKey('loteamento.loteamento_id'), primary_key=True, nullable=False)
    numero = db.Column(db.Integer, primary_key=True, nullable=False)
    quadra = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, loteamento_id, numero, quadra, valor):
        self.loteamento_id = loteamento_id
        self.numero = numero
        self.quadra = quadra
        self.valor = valor