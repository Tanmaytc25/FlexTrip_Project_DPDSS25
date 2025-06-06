import os
from flask import Flask
from datetime import timedelta
from .config import Config
from .extensions import db, migrate
from flask_cors import CORS
from .routes import register_routes

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.abspath('../frontend'),
        template_folder=os.path.abspath('../frontend')
    )

    # Load configuration
    app.config.from_object(Config)

    # Session settings
    app.secret_key = app.config['SECRET_KEY']
    app.permanent_session_lifetime = timedelta(days=7)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ CORS for frontend communication
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # ✅ Register all blueprints/routes
    register_routes(app)

    # ✅ CRUCIAL: Import models to ensure Alembic sees them!
    from app import models

    return app
