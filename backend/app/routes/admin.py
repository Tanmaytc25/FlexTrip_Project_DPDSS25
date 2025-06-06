# backend/app/routes/admin.py

from flask import Blueprint, jsonify
from app.models.user import User
from app.models.trip import Trip
from app.extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@admin_bp.route('/admin/trips', methods=['GET'])
def get_all_trips():
    trips = Trip.query.all()
    return jsonify([trip.to_dict() for trip in trips])

@admin_bp.route('/admin/stats', methods=['GET'])
def get_stats():
    user_count = User.query.count()
    trip_count = Trip.query.count()
    return jsonify({
        "user_count": user_count,
        "trip_count": trip_count
    })
