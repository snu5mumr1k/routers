# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'routers.db')
TEST_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'test.db')

DEFAULT_PAGE_LIMIT = 20

ROUTER_MODELS = [
    'ASUS',
    'Meraki',
    'AirTight',
    'Cisco',
    'Aruba',
    'Aerohive',
    'Ruckus',
]

LOWER_ROUTER_MODELS = {m.lower(): m for m in ROUTER_MODELS}

# XXX: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196  # noqa: E501
SQLALCHEMY_TRACK_MODIFICATIONS = False
