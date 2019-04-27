# -*- coding: utf-8 -*-

from http import HTTPStatus
import json
import pytest

from tests.base import FlaskTestCase
from app import app, db
from app.models import Router, Location


@pytest.fixture
def content(model, state, location_id):
    result = {}
    if model is not None:
        result['model'] = model
    if state is not None:
        result['state'] = state
    if location_id is not None:
        result['location_id'] = location_id
    return result


class TestRouters(FlaskTestCase):
    def __fill_db(self, cnt):
        location = Location(address='Some address')
        location.id = 1
        db.session.add(location)

        routers = {}
        for i in range(cnt):
            router = Router(
                model=app.config['ROUTER_MODELS'][
                    i % len(app.config['ROUTER_MODELS'])
                ],
                location_id=location.id,
            )
            db.session.add(router)
            db.session.commit()
            routers[router.id] = router
        return routers

    def test_router_get(self):
        routers = self.__fill_db(100)
        for router_id in routers:
            routers[router_id] = routers[router_id].data()

        default_limit = 20
        with self.app as context:
            response = context.get('/api/routers')
            data = json.loads(response.data.decode('utf8'))
            assert len(data['routers']) == default_limit
            all_routers = data['routers']

            response = context.get(f'/api/routers?limit={default_limit // 2}')
            data = json.loads(response.data.decode('utf8'))
            assert len(data['routers']) == default_limit // 2
            cur_routers = data['routers']

            limit = default_limit - default_limit // 2
            response = context.get(f'/api/routers?limit={limit}&offset={len(cur_routers)}')
            data = json.loads(response.data.decode('utf8'))
            assert len(data['routers']) == limit

            cur_routers += data['routers']
            models_cnt = 0
            for model in app.config['ROUTER_MODELS']:
                response = context.get(f'/api/routers?limit={len(routers)}&offset=0&model={model}')
                data = json.loads(response.data.decode('utf8'))
                models_cnt += len(data['routers'])
            assert models_cnt == len(routers.keys())

            response = context.get(f'/api/routers?limit={len(routers)}&location_id=1&state=deactivated')
            data = json.loads(response.data.decode('utf8'))
            assert len(data['routers']) == len(routers.keys())

            assert len(cur_routers) == len(all_routers)
            for i in range(len(cur_routers)):
                assert cur_routers[i] == all_routers[i]
            for router_id in routers:
                single_response = context.get(f'/api/routers/{router_id}')
                single_data = json.loads(single_response.data.decode('utf8'))
                assert single_data['router'] == routers[router_id]

    def test_router_get_fail(self):
        with self.app as context:
            response = context.get('/api/routers?limit=test')
            assert response.status_code == HTTPStatus.BAD_REQUEST
            response = context.get('/api/routers?offset=test')
            assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        'model,state,location_id,status_code',
        [
            ('DEFINITELY_NOT_A_MODEL', None, 1, HTTPStatus.BAD_REQUEST),
            (None, None, 1, HTTPStatus.BAD_REQUEST),
            (app.config['ROUTER_MODELS'][0], None, None, HTTPStatus.BAD_REQUEST),
            (app.config['ROUTER_MODELS'][0], None, 1, HTTPStatus.CREATED),
        ]
    )
    def test_router_post(self, model, location_id, status_code, content):
        with self.app as context:
            location = Location(address='Some address')
            location.id = location_id
            db.session.add(location)

            response = context.post(
                '/api/routers',
                data=json.dumps(content),
                content_type='application/json',
            )
            assert response.status_code == status_code, response.data

            if status_code == HTTPStatus.CREATED:
                data = json.loads(response.data.decode('utf8'))
                assert data['router']['model'] == model
                assert data['router']['location_id'] == location_id
                assert data['router']['state'] == 'deactivated'
                assert data['router']['location_id'] == location_id

    def test_router_delete(self):
        with self.app as context:
            router = Router(model=app.config['ROUTER_MODELS'][0], location_id=1)
            db.session.add(router)
            db.session.commit()

            response = context.delete(f'/api/routers/{router.id}')
            assert response.status_code == HTTPStatus.NO_CONTENT
            assert response.data == b''
            assert Router.query.filter(Router.id == router.id)

    @pytest.mark.parametrize(
        'model,state,location_id',
        [
            (app.config['ROUTER_MODELS'][1], None, None),
            (None, Router.State.activated.name, None),
            (None, None, 1),
            (app.config['ROUTER_MODELS'][1], Router.State.activated.name, None),
            (None, Router.State.activated.name, 1),
            (app.config['ROUTER_MODELS'][1], None, 1),
            (app.config['ROUTER_MODELS'][1], Router.State.activated.name, 1),
        ],
    )
    def test_router_put(self, model, state, location_id, content):
        with self.app as context:
            location = Location(address='Some address')
            location.id = 1
            db.session.add(location)

            router = Router(model=app.config['ROUTER_MODELS'][0], location_id=1)
            db.session.add(router)
            db.session.commit()

            response = context.put(
                f'/api/routers/{router.id}',
                data=json.dumps(content),
                content_type='application/json'
            )
            assert response.status_code == HTTPStatus.OK, response.data

            data = json.loads(response.data.decode('utf8'))
            data['router'] == router.data()
            response = context.get(f'/api/routers/{router.id}')
            data = json.loads(response.data.decode('utf8'))
            assert data['router'] == router.data()
