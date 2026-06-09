from __future__ import annotations

from pathlib import Path

from flask import Flask

from .config import Config
from .extensions import db


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if config:
        app.config.update(config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from .routes import bp as main_bp

    app.register_blueprint(main_bp)
    register_cli(app)
    return app


def register_cli(app: Flask) -> None:
    from .models import ensure_schema_compatibility, seed_demo_data

    @app.cli.command("db-init")
    def db_init() -> None:
        """Create database tables."""
        with app.app_context():
            db.create_all()
            ensure_schema_compatibility()
        print("Database tables created.")

    @app.cli.command("seed")
    def seed() -> None:
        """Insert demo data for the single-team workbench."""
        with app.app_context():
            db.create_all()
            ensure_schema_compatibility()
            seed_demo_data()
        print("Demo data inserted.")
