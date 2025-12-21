from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, csrf
from .routes.auth import auth_bp
from .routes.marketplace import market_bp
from .routes.infohub import info_bp
from .routes.admin import admin_bp
from flask_wtf.csrf import generate_csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=generate_csrf)


    # blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(info_bp)
    app.register_blueprint(admin_bp)

    # home
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # CLI commands
    from .cli import register_cli
    register_cli(app)

    return app
