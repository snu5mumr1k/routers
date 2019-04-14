# -*- coding: utf-8 -*-

from flask import Flask

from app.api.ping import api_ping


def create_app(name):
    app = Flask(name)

    app.register_blueprint(api_ping, url_prefix="/api/v1")

    return app
