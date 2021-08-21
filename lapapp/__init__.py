from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'TestingSecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import routes as auth_routes
    app.register_blueprint(auth_routes.auth, url_prefix="/auth")
    from .main import routes as main_routes
    app.register_blueprint(main_routes.main, url_prefix="/main")
    from .api import routes as api_routes
    app.register_blueprint(api_routes.api, url_prefix="/api")

    @app.route("/", methods=["GET"])
    def index():
        return redirect(url_for("main.index"))

    return app