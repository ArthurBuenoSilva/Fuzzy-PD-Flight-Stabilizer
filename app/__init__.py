from flask import Flask

from app.extensions import socketio
from configuration import Configuration


def create_app(config_class=Configuration):
    """Create a new Flask App instance"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    socketio.init_app(app)

    # Register blueprints
    from app.fuzzy_pd import bp

    app.register_blueprint(bp)

    return app
