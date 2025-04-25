from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.user_service import register_user, authenticate_user, get_user_by_email
from app.main import redis_client

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    success, message = register_user(email, password)
    status = 201 if success else 400
    return jsonify({"message": message}), status

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    ip = request.remote_addr

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    attempts_key = f"login_attempts:{ip}"
    if redis_client.get(attempts_key) and int(redis_client.get(attempts_key)) >= 5:
        return jsonify({"message": "Too many login attempts"}), 429

    user = authenticate_user(email, password)
    if not user:
        redis_client.incr(attempts_key)
        redis_client.expire(attempts_key, 600)
        return jsonify({"message": "Invalid credentials"}), 401

    redis_client.delete(attempts_key)
    access_token = create_access_token(identity=email)
    redis_client.setex(f"session:{email}", 3600, access_token)
    return jsonify({"access_token": access_token})

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    email = get_jwt_identity()
    user = get_user_by_email(email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"email": user["email"]})
