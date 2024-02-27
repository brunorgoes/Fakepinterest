from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bancodados.db"
app.config['SECRET_KEY'] = "7c090c652a58bd6824d078823e78640e"
app.config['UPLOAD_FOLDER'] = "static/fotos_post"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes

