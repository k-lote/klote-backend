from datetime import datetime
from .. import db

class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    endereco = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    telefone1 = db.Column(db.String(11), nullable=False)
    telefone2 = db.Column(db.String(11), nullable=False)
    cpf = db.Column(db.String(11), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(11), nullable=True)
    razao_social = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, nome, cpf, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email