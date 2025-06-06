# app/routes/user.py

from flask import Blueprint, session, jsonify
from app.models.user import User
from app.extensions import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict())
