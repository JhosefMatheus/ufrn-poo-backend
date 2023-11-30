from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import SECRET_KEY, MYSQL_CREDENTIALS

app = Flask(__name__)

CORS(app)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{MYSQL_CREDENTIALS['user']}:{MYSQL_CREDENTIALS['password']}@{MYSQL_CREDENTIALS['host']}/{MYSQL_CREDENTIALS['database']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .models import *

from .routes import *