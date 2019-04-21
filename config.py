# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "routers.db")

ROUTER_MODELS = [
    "ASUS",
    "Meraki",
    "AirTight",
    "Cisco",
    "Aruba",
    "Aerohive",
    "Ruckus",
]

# XXX: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
SQLALCHEMY_TRACK_MODIFICATIONS = False
