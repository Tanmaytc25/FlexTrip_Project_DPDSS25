# backend/app/routes/accommodation.py

from flask import Blueprint, request, jsonify
from app.models.accommodation import Accommodation
from app.extensions import db

accommodation_bp = Blueprint('accommodation', __name__)

@accommodation_bp.route('/accommodations', methods=['GET'])
def get_accommodations():
    accommodations = Accommodation.query.all()
    return jsonify([a.to_dict() for a in accommodations])

@accommodation_bp.route('/accommodations/<int:id>', methods=['GET'])
def get_accommodation(id):
    accommodation = Accommodation.query.get_or_404(id)
    return jsonify(accommodation.to_dict())

@accommodation_bp.route('/accommodations', methods=['POST'])
def add_accommodation():
    data = request.json
    new_accommodation = Accommodation(
        name=data['name'],
        address=data['address'],
        cost_per_night=data['cost_per_night'],
        rating=data['rating']
    )
    db.session.add(new_accommodation)
    db.session.commit()
    return jsonify(new_accommodation.to_dict()), 201

@accommodation_bp.route('/accommodations/<int:id>', methods=['PUT'])
def update_accommodation(id):
    accommodation = Accommodation.query.get_or_404(id)
    data = request.json
    accommodation.name = data.get('name', accommodation.name)
    accommodation.address = data.get('address', accommodation.address)
    accommodation.cost_per_night = data.get('cost_per_night', accommodation.cost_per_night)
    accommodation.rating = data.get('rating', accommodation.rating)
    db.session.commit()
    return jsonify(accommodation.to_dict())

@accommodation_bp.route('/accommodations/<int:id>', methods=['DELETE'])
def delete_accommodation(id):
    accommodation = Accommodation.query.get_or_404(id)
    db.session.delete(accommodation)
    db.session.commit()
    return '', 204
