from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return {
        "message": "Authentication route is working!"
    }, 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    required_fields = ["name", "email", "password"]

    for field in required_fields:
        if field not in data:
            return {"message": f"{field} is required"}, 400

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return {"message": "Email already exists"}, 409

    user = User(
        name=data["name"],
        email=data["email"],
        role="admin"
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {
        "message": "Admin registered successfully"
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"message": "Invalid email or password"}, 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "name": user.name
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return {"message": "User not found"}, 404

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }, 200