from app.models import Pedido


def test_checkout_redireciona_se_carrinho_vazio(client):
    response = client.get("/checkout", follow_redirects=True)

    assert response.status_code == 200
    assert "carrinho est".encode("utf-8") in response.data.lower() or b"vazio" in response.data.lower()


def test_checkout_cria_pedido_com_sucesso(client, app, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "2"})

    response = client.post(
        "/checkout",
        data={
            "nome_cliente": "Maria Teste",
            "telefone": "11999999999",
            "endereco": "Rua das Flores, 123",
            "forma_pagamento": "pix",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Pedido confirmado".encode("utf-8") in response.data

    with app.app_context():
        pedidos = Pedido.query.all()
        assert len(pedidos) == 1
        pedido = pedidos[0]
        assert pedido.nome_cliente == "Maria Teste"
        assert float(pedido.total) == 20.00
        assert len(pedido.itens) == 1
        assert pedido.itens[0].quantidade == 2


def test_checkout_esvazia_carrinho_apos_pedido(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "1"})
    client.post(
        "/checkout",
        data={
            "nome_cliente": "João Teste",
            "telefone": "11988888888",
            "endereco": "Av. Principal, 456",
            "forma_pagamento": "cartao",
        },
    )

    cart_response = client.get("/carrinho/")
    assert "Seu carrinho est".encode("utf-8") in cart_response.data


def test_checkout_falha_sem_nome(client, cupcake):
    client.post(f"/carrinho/adicionar/{cupcake.id}", data={"quantidade": "1"})

    response = client.post(
        "/checkout",
        data={
            "nome_cliente": "",
            "telefone": "11988888888",
            "endereco": "Av. Principal, 456",
            "forma_pagamento": "cartao",
        },
    )

    assert response.status_code == 200
    assert "Informe seu nome".encode("utf-8") in response.data


def test_pedido_inexistente_retorna_404(client):
    response = client.get("/pedido/9999")
    assert response.status_code == 404
