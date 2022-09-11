from datetime import datetime
from .. import db

class Cliente_historico(db.Model):
    id_historico = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    def __init__(self, descricao, cliente_id):
        self.descricao = descricao
        self.cliente_id = cliente_id

    def __repr__(self):
        return '<Cliente_historico %r>' % self.id