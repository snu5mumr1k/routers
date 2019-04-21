# -*- coding: utf-8 -*-

import pytest

from app import db
from config import ROUTER_MODELS, ROUTER_STATES
from app.models import Router, Location
from tests.base import FlaskTestCase


def invert_case(s):
    return ''.join(c.lower() if c.isupper() else c.upper() for c in s)


class TestCase(FlaskTestCase):
    def __test_model(self, id, model):
        router = Router.query.filter(Router.id == id).first()
        assert router is not None
        assert router.model == model

    def test_router_create(self):
        for model in ROUTER_MODELS:
            router = Router(model=model, location_id=1)
            db.session.add(router)
            db.session.commit()
            self.__test_model(router.id, model)

        for model in ROUTER_MODELS:
            router = Router(model=invert_case(model), location_id=1)
            db.session.add(router)
            db.session.commit()
            self.__test_model(router.id, model)

        with pytest.raises(ValueError):
            router = Router(model='DEFINITELY_NOT_A_MODEL', location_id=1)

    def test_router_update(self):
        if len(ROUTER_MODELS) > 1:
            model = ROUTER_MODELS[0]
            router = Router(model=model, location_id=1)
            db.session.add(router)
            db.session.commit()
            self.__test_model(router.id, ROUTER_MODELS[0])
            router.model = ROUTER_MODELS[1]
            db.session.add(router)
            db.session.commit()
            self.__test_model(router.id, ROUTER_MODELS[1])

    def test_router_delete(self):
        model = ROUTER_MODELS[0]
        router = Router(model=model, location_id=1)
        db.session.add(router)
        db.session.commit()
        assert Router.query.filter(Router.id == router.id).first() is not None
        db.session.delete(router)
        db.session.commit()
        assert Router.query.filter(Router.id == router.id).first() is None

    def test_router_state(self):
        assert len(ROUTER_STATES)
        model = ROUTER_MODELS[0]
        router = Router(model=model, location_id=1)
        assert router.state == Router.State['deactivated']
        db.session.add(router)
        db.session.commit()
        assert router.state == Router.State['deactivated']
        for state in ROUTER_STATES:
            router.state = state
            assert router.state == state
            db.session.add(router)
            db.session.commit()
            assert router.state == Router.State[state]

    def test_router_location(self):
        model = ROUTER_MODELS[0]
        router = Router(model=model, location_id=1)
        db.session.add(router)
        db.session.commit()
        assert router.location_id == 1
        location = Location(address="USA")
        location.routers.append(router)
        db.session.add(location)
        db.session.commit()
        assert len(location.routers) == 1
        assert location.routers[0].id == router.id
        assert location.id == router.location_id
