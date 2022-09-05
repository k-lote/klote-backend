from datetime import datetime
from .. import db
from .. import ma

class Loteamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    end_cep = db.Column(db.String(8), nullable=False)
    end_logradouro = db.Column(db.String(150), nullable=False)

    def __init__(self, id, nome, end_cep, end_logradouro):
        self.id = id
        self.nome = nome
        self.end_cep = end_cep
        self.end_logradouro = end_logradouro
