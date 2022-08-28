from datetime import datetime
from .. import db
from .. import ma

class Loteamento(db.Model):
    loteamento_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    end_cep = db.Column(db.String(8), nullable=False)
    end_logradouro = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, loteamento_id, nome, end_cep, end_logradouro):
        self.loteamento_id = loteamento_id
        self.nome = nome
        self.end_cep = end_cep
        self.end_logradouro = end_logradouro
