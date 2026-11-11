"""Popula o banco de dados com cupcakes de exemplo.

Uso:
    python -m app.seed
"""

from app import create_app
from app.models import Cupcake, db

PLACEHOLDER_IMG = "/static/img/cupcake-placeholder.svg"

CUPCAKES_EXEMPLO = [
    {
        "nome": "Cupcake de Chocolate",
        "descricao": "Massa de chocolate fofinha com cobertura de brigadeiro.",
        "preco": 8.50,
    },
    {
        "nome": "Cupcake de Baunilha",
        "descricao": "Clássico de baunilha com cobertura de buttercream.",
        "preco": 7.90,
    },
    {
        "nome": "Cupcake Red Velvet",
        "descricao": "Massa aveludada vermelha com cream cheese.",
        "preco": 9.90,
    },
    {
        "nome": "Cupcake de Morango",
        "descricao": "Massa de baunilha com recheio e cobertura de morango.",
        "preco": 9.00,
    },
    {
        "nome": "Cupcake de Limão",
        "descricao": "Massa cítrica de limão siciliano com merengue maçaricado.",
        "preco": 8.90,
    },
    {
        "nome": "Cupcake de Doce de Leite",
        "descricao": "Massa amanteigada com recheio e cobertura de doce de leite.",
        "preco": 9.50,
    },
]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if Cupcake.query.count() > 0:
            print("Banco já populado, nada a fazer.")
            return

        for dados in CUPCAKES_EXEMPLO:
            cupcake = Cupcake(
                nome=dados["nome"],
                descricao=dados["descricao"],
                preco=dados["preco"],
                imagem_url=PLACEHOLDER_IMG,
                disponivel=True,
            )
            db.session.add(cupcake)

        db.session.commit()
        print(f"{len(CUPCAKES_EXEMPLO)} cupcakes inseridos com sucesso.")


if __name__ == "__main__":
    seed()
