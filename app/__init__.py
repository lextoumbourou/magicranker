# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.assets import Environment
from flask.ext.login import LoginManager

from config import AVAILABLE_CONFIGS

db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
login_manager = LoginManager()


def create_app(config):

    # Create and configure the Flash application
    app = Flask(__name__)
    app.config.from_object(AVAILABLE_CONFIGS[config])

    # Initialise Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    assets.init_app(app)
    login_manager.init_app(app)

    # Setup app logging if necessary
    # app.logger.setLevel(logging.INFO)

    # Setup app hooks if necessary
    # @app.before_request
    # def before_request():
    #     pass

    # Setup app error handlers if necessary
    # @app.errorhandler(403)
    # def forbidden(error):
    #     return render_template("403.html"), 403

    # @app.errorhandler(404)
    # def not_found(error):
    #     return render_template("404.html"), 404

    # @app.errorhandler(500)
    # def internal_server_error(error):
    #     return render_template("500.html"), 500

    # Import and register Blueprints
    from .views import front
    from .views import api
    app.register_blueprint(front.mod)
    app.register_blueprint(api.mod)

    return app
