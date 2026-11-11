from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.cart_utils import clear_cart, get_cart_items, get_cart_total
from app.models import ItemPedido, Pedido, db

orders_bp = Blueprint("orders", __name__)

FORMAS_PAGAMENTO = ["dinheiro", "cartao", "pix"]


@orders_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    items = get_cart_items()
    if not items:
        flash("Seu carrinho está vazio. Adicione cupcakes antes de finalizar o pedido.", "warning")
        return redirect(url_for("cart.ver_carrinho"))

    total = get_cart_total(items)

    if request.method == "POST":
        nome_cliente = (request.form.get("nome_cliente") or "").strip()
        telefone = (request.form.get("telefone") or "").strip()
        endereco = (request.form.get("endereco") or "").strip()
        forma_pagamento = (request.form.get("forma_pagamento") or "").strip()

        erros = []
        if not nome_cliente:
            erros.append("Informe seu nome.")
        if not telefone:
            erros.append("Informe seu telefone.")
        if not endereco:
            erros.append("Informe o endereço de entrega.")
        if forma_pagamento not in FORMAS_PAGAMENTO:
            erros.append("Escolha uma forma de pagamento válida.")

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template(
                "checkout.html", items=items, total=total, formas_pagamento=FORMAS_PAGAMENTO
            )

        pedido = Pedido(
            nome_cliente=nome_cliente,
            telefone=telefone,
            endereco=endereco,
            forma_pagamento=forma_pagamento,
            status="recebido",
            total=total,
        )
        for item in items:
            pedido.itens.append(
                ItemPedido(
                    cupcake_id=item["cupcake"].id,
                    quantidade=item["quantidade"],
                    preco_unitario=item["cupcake"].preco,
                )
            )

        db.session.add(pedido)
        db.session.commit()
        clear_cart()

        return redirect(url_for("orders.confirmacao", pedido_id=pedido.id))

    return render_template(
        "checkout.html", items=items, total=total, formas_pagamento=FORMAS_PAGAMENTO
    )


@orders_bp.route("/pedido/<int:pedido_id>")
def confirmacao(pedido_id):
    pedido = db.session.get(Pedido, pedido_id)
    if pedido is None:
        abort(404)
    return render_template("order_confirmation.html", pedido=pedido)
