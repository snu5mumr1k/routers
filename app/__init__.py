# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO(#4): import in the middle of the file is a bad practice
from app.api.locations import api_locations  # noqa: E402
app.register_blueprint(api_locations, url_prefix='/api')

from app.api.routers import api_routers  # noqa: E402
app.register_blueprint(api_routers, url_prefix='/api')


@babel.localeselector
def get_locale():
    return app.config['LANGUAGE']
