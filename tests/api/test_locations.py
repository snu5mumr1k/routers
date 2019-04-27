# -*- coding: utf-8 -*-

from http import HTTPStatus
import json

from tests.base import FlaskTestCase
from app import db
from app.models import Location


class TestLocations(FlaskTestCase):
    def __fill_db(self, cnt):
        locations = {}
        LOCATIONS_ADDRESSES = ['Russia', 'USA', 'France', 'England', 'Germany']
        for i in range(cnt):
            location = Location(
                    address=LOCATIONS_ADDRESSES[i % len(LOCATIONS_ADDRESSES)]
                )
            db.session.add(location)
            db.session.commit()
            locations[location.id] = location
        return locations

    def test_location_get(self):
        locations = self.__fill_db(100)
        for location_id in locations:
            locations[location_id] = locations[location_id].data()

        default_limit = 20
        with self.app as c:
            resp = c.get('/api/locations')
            data = json.loads(resp.data.decode('utf8'))
            assert len(data['locations']) == default_limit
            all_locations = data['locations']

            resp = c.get(
                    '/api/locations?limit={0}'.format(str(default_limit // 2))
                )
            data = json.loads(resp.data.decode('utf8'))
            assert len(data['locations']) == default_limit // 2
            cur_locations = data['locations']
            limit = default_limit - default_limit // 2
            resp = c.get(
                    '/api/locations?limit={0}&offset={1}'.format(
                            limit,
                            str(len(cur_locations))
                        )
                )
            data = json.loads(resp.data.decode('utf8'))
            assert limit == len(data['locations'])
            cur_locations += data['locations']
            assert len(cur_locations) == len(all_locations)

            for location_id in locations.keys():
                resp = c.get(
                        '/api/locations/{0}'.format(
                                str(location_id)
                            )
                    )
                data = json.loads(resp.data.decode('utf8'))
                assert data['location'] == locations[location_id]

            resp = c.get('/api/locations?limit=test')
            assert resp.status_code == HTTPStatus.BAD_REQUEST
            resp = c.get('/api/locations?offset=test')
            assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_location_post(self):
        with self.app as c:
            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': 'Cuba'
                        }
                    )
                )
            assert resp.status_code == HTTPStatus.BAD_REQUEST

            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'not_address': 'Cuba'
                        }
                    )
                )
            assert resp.status_code == HTTPStatus.BAD_REQUEST

            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': 'Cuba'
                        }
                    ),
                    content_type='application/json'
                )
            assert resp.status_code == HTTPStatus.CREATED
            data = json.loads(resp.data.decode('utf8'))
            get_resp = c.get('/api/locations/{0}'.format(
                    str(data['location']['id']))
                )
            get_data = json.loads(get_resp.data.decode('utf8'))
            assert data['location'] == get_data['location']

    def test_location_delete(self):
        with self.app as c:
            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': 'Cuba'
                        }
                    ),
                    content_type='application/json'
                )
            assert resp.status_code == HTTPStatus.CREATED
            data = json.loads(resp.data.decode('utf8'))
            resp = c.delete(
                    '/api/locations/{0}'.format(str(data['location']['id']))
                )
            get_resp = c.get('/api/locations/{0}'.format(
                    str(data['location']['id']))
                )
            assert get_resp.status_code == HTTPStatus.NOT_FOUND

    def test_location_put(self):
        with self.app as c:
            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': 'Cuba'
                        }
                    ),
                    content_type='application/json'
                )
            assert resp.status_code == HTTPStatus.CREATED
            location = json.loads(resp.data.decode('utf8'))['location']
            location['address'] = 'USA'
            resp = c.put(
                    '/api/locations/{0}'.format(str(location['id'])),
                    data=json.dumps(
                        {
                            'address': 'USA'
                        }
                    ),
                    content_type='application/json'
                )
            assert resp.status_code == HTTPStatus.OK
            data = json.loads(resp.data.decode('utf8'))
            assert data['location'] == location
            resp = c.get(
                    '/api/locations/{0}'.format(str(location['id']))
                )
            data = json.loads(resp.data.decode('utf8'))
            assert data['location'] == location
