from datetime import datetime
from .. import db

class Customer(db.Model):
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

    def __init__(self, endereco, status, telefone1, telefone2, cpf, nome, cnpj, razao_social, email):
        self.endereco = endereco
        self.status = status
        self.telefone1 = telefone1
        self.telefone2 = telefone2
        self.cpf = cpf
        self.nome = nome
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.email = email