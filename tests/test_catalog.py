def test_catalogo_lista_cupcakes_disponiveis(client, cupcake):
    response = client.get("/")

    assert response.status_code == 200
    assert cupcake.nome.encode() in response.data


def test_catalogo_nao_lista_cupcakes_indisponiveis(client, cupcake_indisponivel):
    response = client.get("/")

    assert response.status_code == 200
    assert cupcake_indisponivel.nome.encode() not in response.data


def test_catalogo_vazio(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Nenhum cupcake dispon".encode("utf-8") in response.data
