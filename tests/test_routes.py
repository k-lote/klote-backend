#Para ter acesso ao módulo src 
from cgi import test
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src import create_app
from src.models.user import User_klote
from src.routes.allotment import register

#Testar se API inicia com sucesso
def test_init_server(test_client):
    """
    app= create_app()
    client = app.test_client()
    url="/"
    """

    response=test_client.get("/")
     
    assert response.status_code == 302 #redirect

def test_new_user():
    
    user = User_klote("davinovaes.cel@gmail.com", "Password1234", "Davi Novaes", "10029580404", "81995167888")
    assert user.email == "davinovaes.cel@gmail.com"
    assert user.password == "Password1234"
    assert user.name == "Davi Novaes"
    assert user.cpf == "10029580404"
    assert user.phone == "81995167888"

def test_customer_create(test_client):
    response = test_client.post("/customer/register")
    pass

def test_customer_get(test_client):
    response = test_client.get("/customer/get_customers")
    assert response.status_code == 200


