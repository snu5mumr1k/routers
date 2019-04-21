from tests.base import FlaskTestCase
from app import app, db
from app.models import Location
import json


class TestCase(FlaskTestCase):
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
            self.assertEqual(len(data['locations']), default_limit)
            all_locations = data['locations']

            resp = c.get(
                    '/api/locations?limit={0}'.format(str(default_limit // 2))
                )
            data = json.loads(resp.data.decode('utf8'))
            self.assertEqual(len(data['locations']), default_limit // 2)
            cur_locations = data['locations']
            resp = c.get(
                    '/api/locations?limit={0}&offset={1}'.format(
                            str(default_limit - default_limit // 2),
                            str(len(cur_locations))
                        )
                )
            data = json.loads(resp.data.decode('utf8'))
            self.assertEqual(
                    len(data['locations']),
                    default_limit - default_limit // 2
                )
            cur_locations += data['locations']
            self.assertEqual(len(cur_locations), len(all_locations))

            for location_id in locations.keys():
                resp = c.get(
                        '/api/locations/{0}'.format(
                                str(location_id)
                            )
                    )
                data = json.loads(resp.data.decode('utf8'))
                self.assertDictEqual(
                        data['location'], locations[location_id]
                    )

            resp = c.get('/api/locations?limit=test')
            self.assertEqual(resp.status_code, 400)
            resp = c.get('/api/locations?offset=test')
            self.assertEqual(resp.status_code, 400)

    def test_location_post(self):
        with self.app as c:
            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': "Cuba"
                        }
                    )
                )
            self.assertEqual(resp.status_code, 400)

            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'not_address': "Cuba"
                        }
                    )
                )
            self.assertEqual(resp.status_code, 400)

            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': 'Cuba'
                        }
                    ),
                    content_type='application/json'
                )
            self.assertEqual(resp.status_code, 201)
            data = json.loads(resp.data.decode('utf8'))
            get_resp = c.get('/api/locations/{0}'.format(
                    str(data['location']['id']))
                )
            get_data = json.loads(get_resp.data.decode('utf8'))
            self.assertDictEqual(data['location'], get_data['location'])

    def test_location_delete(self):
        with self.app as c:
            resp = c.post(
                    '/api/locations',
                    data=json.dumps(
                        {
                            'address': "Cuba"
                        }
                    ),
                    content_type='application/json'
                )
            self.assertEqual(resp.status_code, 201)
            data = json.loads(resp.data.decode('utf8'))
            resp = c.delete(
                    '/api/locations/{0}'.format(str(data['location']['id']))
                )
            get_resp = c.get('/api/locations/{0}'.format(
                    str(data['location']['id']))
                )
            self.assertEqual(get_resp.status_code, 404)

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
            self.assertEqual(resp.status_code, 201)
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
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data.decode('utf8'))
            self.assertDictEqual(data['location'], location)
            resp = c.get(
                    '/api/locations/{0}'.format(str(location['id']))
                )
            data = json.loads(resp.data.decode('utf8'))
            self.assertDictEqual(data['location'], location)

    def get_desc(self):
        return 'Testing locations api functionality'
