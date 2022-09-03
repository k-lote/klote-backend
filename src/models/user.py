from datetime import datetime
from .. import db
from .. import ma
import re

user_id_seq = db.Sequence('user_id_seq', metadata=db.MetaData())

class User_klote(db.Model):
    user_id = db.Column(db.Integer, user_id_seq, primary_key=True, unique=True, )
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    phone = db.Column(db.String(11), unique=True)
    #first_login = db.Column(db.Boolean, nullable=False, default=True)
    #is_admin = db.Column(db.Boolean, nullable=False, default=False)
    #created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #token = db.Column(db.String(150), unique=True)


    def validates_password(password):
        if len(password) < 8:
            return False, "A senha deve conter no mínimo 8 caracteres"
        if not any(char.isdigit() for char in password):
            return False, "A senha deve conter pelo menos um número"
        if not any(char.isupper() for char in password):
            return False, "A senha deve conter pelo menos uma letra maiúscula"
        if not any(char.islower() for char in password):
            return False, "A senha deve conter pelo menos uma letra minúscula"
        
        return True, None
        
    def validates_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "E-mail inválido"
        return True, None
        
    def validates_cpf(cpf):
        if not re.match(r"[0-9]{11}", cpf):
            return False, "CPF inválido"
        return True, None
    
    def validates_phone(phone):
        if not re.match(r"[0-9]{11}", phone):
            return False, "Telefone inválido"
        return True, None
    
    def validates_name(name):
        if not re.match(r"[a-zA-Z ]+", name):
            return False, "Nome inválido"
        return True, None
    
    def __init__(self, email, password, name, cpf, phone):
        #self.user_id = user_id
        self.email = email
        self.password = password
        self.name = name
        self.cpf = cpf
        self.phone = phone

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'email', 'name', 'cpf', 'phone')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
