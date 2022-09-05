from datetime import datetime
from .. import db
from .. import ma

class Acesso(db.Model):
    __tablename__ = 'acesso'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    loteamento_id = db.Column(db.Integer, db.ForeignKey('loteamento.id'), primary_key=True, nullable=False)

    def __init__(self, user_id, loteamento_id):
        self.user_id = user_id
        self.loteamento_id = loteamento_id