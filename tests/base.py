# -*- coding: utf-8 -*-

from app import app, db


class FlaskTestCase:
    def setup(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_DATABASE_URL']
        self.app = app.test_client()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
