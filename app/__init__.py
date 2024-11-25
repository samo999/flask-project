# # app/__init__.py
# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     # Register routes
#     from .routes import main
#     app.register_blueprint(main)

#     return app

#############
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprints
    from .routes import location_airport  # Ensure the blueprint name matches
    app.register_blueprint(location_airport, url_prefix='/api')

    return app
