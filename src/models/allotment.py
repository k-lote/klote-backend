from datetime import datetime
from venv import create
from .. import db
from .. import ma

allotment_id_seq = db.Sequence('allotment_id_seq', metadata=db.MetaData())

class Allotment(db.Model):
    __tablename__ = 'allotment'
    id = db.Column(db.Integer, allotment_id_seq, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, cep, address, img_url, logo_url):
        self.name = name
        self.cep = cep
        self.address = address
        self.img_url = img_url
        self.logo_url = logo_url

class AllotmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'cep', 'address', 'img_url')

allotment_schema = AllotmentSchema()
allotments_schema = AllotmentSchema(many=True)