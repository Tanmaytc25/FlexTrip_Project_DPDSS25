# backend/app/routes/suggest.py

from flask import Blueprint, request, jsonify
#from app.services.suggestions import generate_suggestions

suggest_bp = Blueprint('suggest', __name__)

@suggest_bp.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    user_preferences = data.get('preferences', {})
    location = data.get('location', '')
    days = data.get('days', 1)

    suggestions = generate_suggestions(location, user_preferences, days)
    return jsonify(suggestions)
