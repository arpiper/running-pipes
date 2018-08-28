from ..routes.users import user_bp
from ..routes.api import api_bp
from ..routes.auth import auth_bp

def init_app(app):
    # register the route blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
