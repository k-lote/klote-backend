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