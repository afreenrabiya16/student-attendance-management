from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app)

    @app.route("/")
    def home():
        return {
            "message": "Backend Working 🚀"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)