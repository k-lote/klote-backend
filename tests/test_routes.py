import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src import create_app

def test_init_server():
    app= create_app()
    client = app.test_client()
    url="/"

    response=client.get(url)
    
    assert response.get_data() == b'API is running'
    assert response.status_code == 200