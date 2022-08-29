from datetime import datetime
from .. import db

class Lote_historico(db.Model):
    id_historico = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    loteamento_id = db.Column(db.Integer, db.ForeignKey('loteamento.loteamento_id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, loteamento_id, numero, descricao):
        self.loteamento_id = loteamento_id
        self.numero = numero
        self.descricao = descricao