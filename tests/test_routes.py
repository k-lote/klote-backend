#Para ter acesso ao módulo src 
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src import create_app
from src.models.user import User_klote

#Testar se API inicia com sucesso
def test_init_server(test_client):
    """
    app= create_app()
    client = app.test_client()
    url="/"
    """

    response=test_client.get("/")
     
    assert response.get_data() == b'API is running'
    assert response.status_code == 200

def test_new_user():
    
    user = User_klote("davinovaes.cel@gmail.com", "Password1234", "Davi Novaes", "10029580404", "81995167888")
    assert user.email == "davinovaes.cel@gmail.com"
    assert user.password == "Password1234"
    assert user.name == "Davi Novaes"
    assert user.cpf == "10029580404"
    assert user.phone == "81995167888"
