from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'aunlken fslidjf @498r997 !*$(%) 249slkdjf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Trip, MapData  # Add MapData here

    with app.app_context():
        create_database()  # Create the database if it does not exist

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    if not path.exists('wbsite/' + DB_NAME):
        db.create_all()
        print("Database created!")