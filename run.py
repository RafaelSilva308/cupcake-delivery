import os

from config import BASE_DIR
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
