from flask import Flask
from flask_config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"

db = SQLAlchemy(app)
migrate = Migrate(app,db)


from app import route,models
