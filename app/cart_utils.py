from flask import session

from app.models import Cupcake

CART_SESSION_KEY = "cart"


def get_raw_cart():
    """Retorna o carrinho cru salvo na sessão: {str(cupcake_id): quantidade}."""
    return session.get(CART_SESSION_KEY, {})


def add_to_cart(cupcake_id, quantidade=1):
    cart = get_raw_cart()
    key = str(cupcake_id)
    cart[key] = cart.get(key, 0) + quantidade
    session[CART_SESSION_KEY] = cart


def update_quantity(cupcake_id, quantidade):
    cart = get_raw_cart()
    key = str(cupcake_id)
    if quantidade <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantidade
    session[CART_SESSION_KEY] = cart


def remove_from_cart(cupcake_id):
    cart = get_raw_cart()
    cart.pop(str(cupcake_id), None)
    session[CART_SESSION_KEY] = cart


def clear_cart():
    session.pop(CART_SESSION_KEY, None)


def get_cart_items():
    """Resolve o carrinho da sessão em uma lista de itens com dados do cupcake e subtotal."""
    cart = get_raw_cart()
    if not cart:
        return []

    ids = [int(cupcake_id) for cupcake_id in cart.keys()]
    cupcakes = {c.id: c for c in Cupcake.query.filter(Cupcake.id.in_(ids)).all()}

    items = []
    for cupcake_id, quantidade in cart.items():
        cupcake = cupcakes.get(int(cupcake_id))
        if cupcake is None:
            continue
        subtotal = cupcake.preco * quantidade
        items.append(
            {
                "cupcake": cupcake,
                "quantidade": quantidade,
                "subtotal": subtotal,
            }
        )
    return items


def get_cart_total(items=None):
    if items is None:
        items = get_cart_items()
    return sum((item["subtotal"] for item in items), start=0)
