from flask import Flask
from sqlalchemy import create_engine

from healingpawsapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
# from werkzeug.utils import ImmutableDict
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)

#engine = create_engine(db, echo=True)
#self.conn = engine.connect()

from healingpawsapp import routes, models

