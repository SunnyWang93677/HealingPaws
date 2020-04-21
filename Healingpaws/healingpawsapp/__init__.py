from flask import Flask
from sqlalchemy import create_engine

from healingpawsapp.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#engine = create_engine(db, echo=True)
#self.conn = engine.connect()
from healingpawsapp import routes, models

