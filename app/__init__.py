from flask import Flask

from config import Config
from app.models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.controllers.catalog import catalog_bp
    from app.controllers.cart import cart_bp
    from app.controllers.orders import orders_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    return app
