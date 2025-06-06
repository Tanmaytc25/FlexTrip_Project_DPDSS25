from flask import Blueprint, request, jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from datetime import time, datetime, timedelta
from app.extensions import db
from app.models.poi import PointOfInterest as POI
from calendar_utils import add_trip_events  # 📅 Calendar integration

microtrip_bp = Blueprint("microtrip", __name__, url_prefix="/api/microtrip")

@microtrip_bp.route("/generate", methods=["POST"])
def generate_microtrip():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Request payload is missing or invalid JSON"}), 400

        location = data.get("current_location")
        interests = data.get("interests", [])
        budget = data.get("budget")
        add_to_calendar = data.get("add_to_calendar", False)  # 📅 Optional flag

        print(f"✅ Received microtrip request: location={location}, interests={interests}, budget={budget}, calendar={add_to_calendar}")

        if not location or not interests:
            return jsonify({"error": "Both 'current_location' and 'interests' are required."}), 400

        available_start = time(9, 0)
        max_total_duration = 300  # 5 hours
        max_stops = 5

        # Query POIs with interest overlap and matching location
        try:
            query = db.session.query(POI).filter(
                func.lower(POI.location) == location.lower(),
                POI.interests.op("&&")(interests)
            )
            pois = query.order_by(POI.id).all()
        except SQLAlchemyError as db_error:
            print(f"⚠️ SQLAlchemy DB error: {db_error}")
            return jsonify({"error": f"Database error: {str(db_error)}"}), 500

        selected = []
        total_time = 0
        current_time = datetime.combine(datetime.today(), available_start)

        for poi in pois:
            duration = poi.duration_minutes or 60
            if total_time + duration > max_total_duration:
                break

            start_time = current_time
            end_time = current_time + timedelta(minutes=duration)

            selected.append({
                "name": poi.name,
                "description": poi.description or "",
                "location": poi.location,
                "interests": poi.interests,
                "duration_minutes": duration,
                "estimated_cost": poi.estimated_cost or 10.0,
                "price_range": poi.price_range or "€",
                "opening_time": str(poi.opening_time) if poi.opening_time else "09:00",
                "closing_time": str(poi.closing_time) if poi.closing_time else "18:00",
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            })

            total_time += duration
            current_time = end_time
            if len(selected) >= max_stops:
                break

        print(f"✅ Returning {len(selected)} POIs.")

        if add_to_calendar and selected:
            calendar_urls = add_trip_events(selected)
            print("📅 Events successfully added to Google Calendar.")
            return jsonify({"recommended": selected, "calendar_urls": calendar_urls}), 200

        return jsonify({"recommended": selected}), 200

    except Exception as e:
        print(f"❌ Unexpected error in /api/microtrip/generate: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500
