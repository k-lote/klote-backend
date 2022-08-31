from datetime import datetime
from .. import db

class Parcela(db.Model):
    cod_parcela = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    data = db.Column(db.DateTime)
    status = db.Column(db.String(255))
    numero_da_parcela = db.Column(db.Integer)
    loteamento_id = db.Column(db.Integer, db.ForeignKey('compra.loteamento_id'))
    numero = db.Column(db.Integer, db.ForeignKey('compra.numero'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    def __init__(self, valor, data_vencimento, data_pagamento, status, cliente_id):
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.data_pagamento = data_pagamento
        self.status = status
        self.cliente_id = cliente_id

    def __repr__(self):
        return '<Parcela %r>' % self.id