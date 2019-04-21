# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.api.locations import api_locations
app.register_blueprint(api_locations, url_prefix='/api')

from app import models
