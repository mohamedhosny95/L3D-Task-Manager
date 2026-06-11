from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO
import cloudinary
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
socketio = SocketIO()


def create_app(config_name=None):
    import os
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        # FLASK_ENV=development maps to our 'development' key
        if config_name not in config:
            config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, async_mode='gevent', cors_allowed_origins='*')

    # Flask-Login settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Cloudinary config
    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET'),
    )

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    # Register socket events
    from app.sockets import events  # noqa: F401

    return app
