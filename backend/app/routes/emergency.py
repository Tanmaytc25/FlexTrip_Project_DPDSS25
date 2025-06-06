# backend/app/routes/emergency.py

from flask import Blueprint, jsonify
from app.models.emergency import Emergency
from app.extensions import db

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/emergency_contacts', methods=['GET'])
def get_emergency_contacts():
    contacts = Emergency.query.all()
    results = [contact.to_dict() for contact in contacts]
    return jsonify(results), 200
