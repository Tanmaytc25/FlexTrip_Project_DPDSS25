# backend/app/routes/trip.py

from flask import Blueprint, request, jsonify
from app.models.trip import Trip
from app.extensions import db

trip_bp = Blueprint('trip', __name__)

@trip_bp.route('/trips', methods=['GET'])
def get_all_trips():
    trips = Trip.query.all()
    return jsonify([trip.to_dict() for trip in trips])

@trip_bp.route('/trip/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return jsonify(trip.to_dict())

@trip_bp.route('/trip', methods=['POST'])
def create_trip():
    data = request.get_json()
    trip = Trip(**data)
    db.session.add(trip)
    db.session.commit()
    return jsonify(trip.to_dict()), 201

@trip_bp.route('/trip/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(trip, key, value)
    db.session.commit()
    return jsonify(trip.to_dict())

@trip_bp.route('/trip/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': 'Trip deleted'})
