from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Добавьте импорт Flask-Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
migrate = Migrate()  # Создайте объект Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # Инициализируйте Migrate с app и db
    login_manager.init_app(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
