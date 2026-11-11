from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.cart_utils import (
    add_to_cart,
    get_cart_items,
    get_cart_total,
    remove_from_cart,
    update_quantity,
)
from app.models import Cupcake

cart_bp = Blueprint("cart", __name__, url_prefix="/carrinho")


@cart_bp.route("/")
def ver_carrinho():
    items = get_cart_items()
    total = get_cart_total(items)
    return render_template("cart.html", items=items, total=total)


@cart_bp.route("/adicionar/<int:cupcake_id>", methods=["POST"])
def adicionar(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    if not cupcake.disponivel:
        abort(400)

    quantidade = request.form.get("quantidade", default=1, type=int)
    if quantidade is None or quantidade < 1:
        quantidade = 1

    add_to_cart(cupcake_id, quantidade)
    flash(f"{cupcake.nome} adicionado ao carrinho.", "success")
    return redirect(request.referrer or url_for("catalog.index"))


@cart_bp.route("/atualizar/<int:cupcake_id>", methods=["POST"])
def atualizar(cupcake_id):
    quantidade = request.form.get("quantidade", default=0, type=int)
    if quantidade is None:
        quantidade = 0
    update_quantity(cupcake_id, quantidade)
    return redirect(url_for("cart.ver_carrinho"))


@cart_bp.route("/remover/<int:cupcake_id>", methods=["POST"])
def remover(cupcake_id):
    remove_from_cart(cupcake_id)
    flash("Item removido do carrinho.", "info")
    return redirect(url_for("cart.ver_carrinho"))
