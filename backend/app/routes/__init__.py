# backend/app/routes/__init__.py

from app.routes.auth import auth_bp
from app.routes.trip import trip_bp
from app.routes.suggest import suggest_bp
from app.routes.microtrip import microtrip_bp
from app.routes.accommodation import accommodation_bp
from app.routes.emergency import emergency_bp
from app.routes.oauth import oauth_bp
from app.routes.admin import admin_bp
from app.routes.user import user_bp

def register_routes(app):
    """Register all route blueprints with correct prefixes."""
    app.register_blueprint(auth_bp)           # /api/auth
    app.register_blueprint(trip_bp)           # /api/trips
    app.register_blueprint(suggest_bp)        # /api/suggest
    app.register_blueprint(microtrip_bp)      # /api/microtrip
    app.register_blueprint(accommodation_bp)  # /api/accommodation
    app.register_blueprint(emergency_bp)      # /api/emergency
    app.register_blueprint(oauth_bp)          # /api/oauth
    app.register_blueprint(admin_bp)          # /api/admin
    app.register_blueprint(user_bp)           # /api/user
