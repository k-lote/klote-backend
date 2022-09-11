from datetime import datetime
from .. import db
from .. import ma

class Allotment_access(db.Model):
    __tablename__ = 'allotment_access'
    user_id = db.Column(db.Integer, db.ForeignKey('user_klote.user_id'), primary_key=True, nullable=False)
    allotment_id = db.Column(db.Integer, db.ForeignKey('allotment.id'), primary_key=True, nullable=False)

    def __init__(self, user_id, allotment_id):
        self.user_id = user_id
        self.allotment_id = allotment_id

class Allotment_accessSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'allotment_id')
    
allotment_access_schema = Allotment_accessSchema()
allotments_access_schema = Allotment_accessSchema(many=True)