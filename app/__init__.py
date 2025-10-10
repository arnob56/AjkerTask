import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import secrets

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Load .env if present (local dev)

    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (mostly for local dev)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Generate a default secret key if FLASK_SECRET_KEY not set
    default_secret = secrets.token_hex(16)

    # --- CONFIGURATION ---
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable not set! "
            "Set it in Vercel Dashboard or your local .env file."
        )

    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", default_secret),
        SQLALCHEMY_DATABASE_URI=DATABASE_URL,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # --- Initialize extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Flask-Login config
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # --- Blueprints ---
    from .auth import auth_bp
    from .routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # --- Create tables ---
    with app.app_context():
        from . import models  # ensure models are imported
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print("❌ Error creating tables:", e)
            raise

    # --- Debug ---
    print("Database URL loaded:", bool(app.config['SQLALCHEMY_DATABASE_URI']))
    print("Secret Key set:", bool(app.config['SECRET_KEY']))

    return app
