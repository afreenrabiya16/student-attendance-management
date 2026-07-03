from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, bcrypt, jwt
from models.user import User
from models.student import Student
from models.attendance import Attendance
from routes.auth import auth_bp
from routes.student import student_bp

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
            "message": "Backend Working "
        }

    with app.app_context():
        db.create_all()
       
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(student_bp, url_prefix="/api/students")

    print("\nRegistered Routes:")
    print(app.url_map)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)