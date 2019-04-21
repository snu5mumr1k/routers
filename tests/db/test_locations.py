# -*- coding: utf-8 -*-

from app import db
from app.models import Location, Router
from config import ROUTER_MODELS
from tests.base import FlaskTestCase


class TestLocations(FlaskTestCase):
    def test_location_create(self):
        address = "Russia, Moscow, Red Square"
        location = Location(address=address)
        db.session.add(location)
        db.session.commit()
        assert len(Location.query.filter(Location.address == address).all())
        assert len(Location.query.filter(Location.id == location.id).all())
        created_address = Location.query.filter(
            Location.id == location.id
        ).first().address
        assert address == created_address

    def test_location_update(self):
        address = "Russia, Moscow"
        location = Location(address=address)
        db.session.add(location)
        db.session.commit()
        location_id = location.id
        assert len(Location.query.filter(Location.address == address).all())
        assert len(Location.query.filter(Location.id == location_id).all())
        address += ", Red Square"
        location.address = address
        db.session.add(location)
        db.session.commit()
        assert len(Location.query.filter(Location.address == address).all())
        assert len(Location.query.filter(Location.id == location_id).all())

    def test_location_delete(self):
        address = "Russia, Moscow, Red Square"
        location = Location(address=address)
        db.session.add(location)
        db.session.commit()
        assert Location.query.filter(Location.id == location.id).first() is not None
        db.session.delete(location)
        db.session.commit()
        assert Location.query.filter(Location.id == location.id).first() is None

    def test_location_routers(self):
        assert len(ROUTER_MODELS)
        routers_cnt = 15
        address1 = "Russia, Moscow, Red Square"
        address2 = "Russia, Moscow, Red Square 2"
        for i in range(routers_cnt):
            db.session.add(Router(ROUTER_MODELS[i % len(ROUTER_MODELS)], 1))
        db.session.add(Location(address=address1))
        db.session.add(Location(address=address2))
        db.session.commit()
        start_location = Location.query.filter(
            Location.id == 1
        ).first()
        cur_location = Location.query.filter(
            Location.address == address2
        ).first()
        routers = Router.query.all()
        assert start_location
        assert cur_location
        assert len(routers) == routers_cnt
        assert len(start_location.routers) == routers_cnt
        for router in routers[:(routers_cnt // 2)]:
            cur_location.routers.append(router)
        db.session.add(cur_location)
        db.session.commit()
        start_location = Location.query.filter(
            Location.id == 1
        ).first()
        cur_location = Location.query.filter(
            Location.address == address2
        ).first()
        assert len(start_location.routers) == routers_cnt - routers_cnt // 2
        assert len(cur_location.routers) == routers_cnt // 2

    def get_desc(self):
        return 'Testing locations db functionality'
