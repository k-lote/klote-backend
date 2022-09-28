#Para ter acesso ao módulo src 
import sys
import pytest
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src import create_app
from src.models.user import User_klote

@pytest.mark.parametrize(
    "password,valid",
    [
        ("Acde12345", True),
        ("ABCDE12345", False),
        ("Ac1dslkd", True),
        ("a234", False),
        ("", False),
        ("Abcde",False)

    ]
)
def test_new_user(password,valid):
    #given
    
    
    try:
        #when
        if User_klote.validates_password(password)[0] is False:
            raise "Password error"
        user = User_klote("davinovaes.cel@gmail.com", password, "Davi Novaes", "10029580404", "81995167888", False, False)
        
        #then
        assert valid
        assert user.email == "davinovaes.cel@gmail.com"
        assert user.password == password
        assert user.name == "Davi Novaes"
        assert user.cpf == "10029580404"
        assert user.phone == "81995167888"
    except:
        assert not valid

def test_new_user_nopassworderror():
    try:
        user = User_klote("davinovaes.cel@gmail.com", "Davi Novaes", "10029580404", "81995167888", False, False)
        assert False
    except:
        pass