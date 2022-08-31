from datetime import datetime
from .. import db

class Compra(db.Model):
    loteamento_id = db.Column(db.Integer, db.ForeignKey('lote.loteamento_id'), primary_key=True)
    numero = db.Column(db.Integer, db.ForeignKey('lote.numero') ,primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.cliente_id'))
    data_compra = db.Column(db.DateTime)

    def __init__(self, loteamento_id, numero, cliente_id, data_compra):
        self.loteamento_id = loteamento_id
        self.numero = numero
        self.cliente_id = cliente_id
        self.data_compra = data_compra

    def __repr__(self):
        return '<Compra %r>' % self.id