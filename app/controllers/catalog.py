from flask import Blueprint, render_template

from app.models import Cupcake

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/")
def index():
    cupcakes = Cupcake.query.filter_by(disponivel=True).order_by(Cupcake.nome).all()
    return render_template("catalog.html", cupcakes=cupcakes)
