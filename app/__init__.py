from flask import Flask
from flask_config import Config
from flask_login import LoginManager
import dbms_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


login = LoginManager()
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)




from app import route,models
