from flask import Flask
from sqlalchemy import create_engine

from healingpawsapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from flask_babel import Babel
from werkzeug import ImmutableDict
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)

#engine = create_engine(db, echo=True)
#self.conn = engine.connect()

from healingpawsapp import routes, models

