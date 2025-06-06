import os
import json
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db  
from app.models.oauth_token import OAuthToken
from app.models.trip import Trip
from app.models.itinerary import ItineraryItem

oauth_bp = Blueprint("oauth", __name__)

# 🔐 Environment Config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPE = "https://www.googleapis.com/auth/calendar.events"
GOOGLE_AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_CALENDAR_API = "https://www.googleapis.com/calendar/v3"

# ----------------------------------------------
# Step 1: Redirect user to Google's OAuth 2.0 server
# ----------------------------------------------
@oauth_bp.route("/calendar/connect", methods=["GET"])
@jwt_required()
def connect_calendar():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": GOOGLE_SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    return redirect(f"{GOOGLE_AUTH_BASE}?{urlencode(params)}")

# ----------------------------------------------
# Step 2: Handle callback and store tokens
# ----------------------------------------------
@oauth_bp.route("/calendar/callback", methods=["GET"])
@jwt_required()
def calendar_callback():
    code = request.args.get("code")
    user_id = get_jwt_identity()

    if not code:
        return jsonify({"error": "Authorization code missing."}), 400

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        return jsonify({"error": "Failed to retrieve token.", "details": token_data}), 400

    oauth_token = OAuthToken.query.filter_by(user_id=user_id).first()
    if not oauth_token:
        oauth_token = OAuthToken(user_id=user_id)

    oauth_token.access_token = token_data["access_token"]
    oauth_token.refresh_token = token_data.get("refresh_token", oauth_token.refresh_token)
    oauth_token.expires_at = datetime.utcnow() + timedelta(seconds=token_data["expires_in"])

    db.session.add(oauth_token)
    db.session.commit()

    return redirect("http://localhost:3000/dashboard.html")  # ✅ Frontend redirect after success

# ----------------------------------------------
# Step 3: Sync trip itinerary to Google Calendar
# ----------------------------------------------
@oauth_bp.route("/calendar/sync/<int:trip_id>", methods=["POST"])
@jwt_required()
def sync_trip_to_calendar(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()

    if not trip:
        return jsonify({"error": "Trip not found."}), 404

    token = OAuthToken.query.filter_by(user_id=user_id).first()
    if not token or not token.refresh_token:
        return jsonify({"error": "Google Calendar is not connected or missing refresh token."}), 401

    # Refresh the access token using refresh_token
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": token.refresh_token,
        "grant_type": "refresh_token"
    }

    token_resp = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    if token_resp.status_code != 200:
        return jsonify({"error": "Failed to refresh token.", "details": token_resp.json()}), 400

    new_access_token = token_resp.json().get("access_token")
    if not new_access_token:
        return jsonify({"error": "Missing access token in refresh response."}), 400

    token.access_token = new_access_token
    token.expires_at = datetime.utcnow() + timedelta(seconds=token_resp.json().get("expires_in", 3600))
    db.session.commit()

    # Now use the new access token to create events
    headers = {
        "Authorization": f"Bearer {new_access_token}",
        "Content-Type": "application/json"
    }

    items = ItineraryItem.query.filter_by(trip_id=trip.id).all()
    for item in items:
        start_dt = datetime.combine(trip.start_date + timedelta(days=item.day - 1),
                                    datetime.strptime(item.start_time or "09:00", "%H:%M").time())
        end_dt = datetime.combine(trip.start_date + timedelta(days=item.day - 1),
                                  datetime.strptime(item.end_time or "11:00", "%H:%M").time())

        event = {
            "summary": item.title,
            "location": item.location,
            "description": item.description,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "UTC"
            }
        }

        response = requests.post(
            f"{GOOGLE_CALENDAR_API}/calendars/primary/events",
            headers=headers,
            json=event
        )

        if response.status_code not in (200, 201):
            return jsonify({
                "error": "Failed to create calendar event.",
                "event": event,
                "response": response.json()
            }), 400

    return jsonify({"message": "Trip synced to Google Calendar successfully."})

# ----------------------------------------------
# Step 4: Check if calendar is connected
# ----------------------------------------------
@oauth_bp.route("/calendar/status", methods=["GET"])
@jwt_required()
def check_calendar_connection():
    user_id = get_jwt_identity()
    token = OAuthToken.query.filter_by(user_id=user_id).first()

    if token and token.access_token and token.expires_at > datetime.utcnow():
        return jsonify({"connected": True})
    else:
        return jsonify({"connected": False})
