import pytest

from app import create_app
from app.models import Cupcake, db
from config import TestConfig


@pytest.fixture()
def app():
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def cupcake(app):
    c = Cupcake(
        nome="Cupcake de Teste",
        descricao="Cupcake usado nos testes automatizados.",
        preco=10.00,
        imagem_url="/static/img/cupcake-placeholder.svg",
        disponivel=True,
    )
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture()
def cupcake_indisponivel(app):
    c = Cupcake(
        nome="Cupcake Esgotado",
        descricao="Cupcake sem estoque.",
        preco=5.00,
        imagem_url="/static/img/cupcake-placeholder.svg",
        disponivel=False,
    )
    db.session.add(c)
    db.session.commit()
    return c
