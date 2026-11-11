from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cupcake(db.Model):
    __tablename__ = "cupcake"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255), nullable=False, default="")
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False, default="")
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

    itens_pedido = db.relationship("ItemPedido", back_populates="cupcake")

    def __repr__(self):
        return f"<Cupcake {self.id} {self.nome}>"


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    forma_pagamento = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="recebido")
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    itens = db.relationship(
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Pedido {self.id} {self.nome_cliente}>"


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    cupcake_id = db.Column(db.Integer, db.ForeignKey("cupcake.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = db.relationship("Pedido", back_populates="itens")
    cupcake = db.relationship("Cupcake", back_populates="itens_pedido")

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __repr__(self):
        return f"<ItemPedido pedido={self.pedido_id} cupcake={self.cupcake_id} qtd={self.quantidade}>"
