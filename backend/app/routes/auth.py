# backend/app/routes/auth.py

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

SESSION_TIMEOUT = timedelta(days=7)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = db.session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return jsonify({"message": "Username or email already in use"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = db.session.query(User).filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        session.permanent = True
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})
