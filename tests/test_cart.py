def test_adicionar_ao_carrinho(client, cupcake):
    response = client.post(
        f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "2"}, follow_redirects=True
    )

    assert response.status_code == 200

    cart_response = client.get("/carrinho/")
    assert cupcake.nome.encode() in cart_response.data
    assert "R$ 20.00".encode() in cart_response.data


def test_adicionar_quantidade_invalida_usa_um(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "-5"})

    cart_response = client.get("/carrinho/")
    assert "R$ 10.00".encode() in cart_response.data


def test_adicionar_cupcake_indisponivel_falha(client, cupcake_indisponivel):
    response = client.post(f"/carrinho/adicionar/{cupcake_indisponivel.id}")

    assert response.status_code == 400


def test_atualizar_quantidade(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "1"})
    client.post(f"/carrinho/atualizar/{cupcake.id}", data={"quantidade": "3"})

    cart_response = client.get("/carrinho/")
    assert "R$ 30.00".encode() in cart_response.data


def test_atualizar_quantidade_zero_remove_item(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "1"})
    client.post(f"/carrinho/atualizar/{cupcake.id}", data={"quantidade": "0"})

    cart_response = client.get("/carrinho/")
    assert "Seu carrinho est".encode("utf-8") in cart_response.data


def test_remover_do_carrinho(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "1"})
    client.post(f"/carrinho/remover/{cupcake.id}")

    cart_response = client.get("/carrinho/")
    assert "Seu carrinho est".encode("utf-8") in cart_response.data
