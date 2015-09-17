#!flask/bin/python
"""
Copyright (c) 2015 Aritz Bilbao, Aitor Almeida
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
@author: "Aritz Bilbao, Aitor Almeida"
@contact: aritzbilbao@deusto.es, aitor.almeida@deusto.es
"""


import unittest
from app import app, db
from app import models, views
from os.path import isfile
from utils import format_filename
import json
from time import mktime
from coverage import coverage
from datetime import datetime


cov = coverage(source=['./'])


class TestCase(unittest.TestCase):

    def setUp(self):
        cov.start()

        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sonopa:sonopa@localhost/sonopatests'
        app.config.pop('SQLALCHEMY_MIGRATE_URI', None)
        self.app = app.test_client()

        assert not db.engine.dialect.has_table(db.session, 'location')

        views.init_db()

        assert db.engine.dialect.has_table(db.session, 'location')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        cov.stop()
        cov.save()
        cov.html_report(directory='./tests_coverage_{0}'.format(datetime.now()))

    def login(self):
        resp = self.app.post('/login', data=dict(username='user', password='user'))
        assert 'Welcome' in resp.data

    def logout(self):
        resp = self.app.get('/logout')
        assert 'Bye' in resp.data

    def login_logout_authentication(self):
        resp = self.app.get('/get_last')
        assert 'Unauthorized' in resp.data
        self.login()
        resp = self.app.get('/get_last')
        assert not 'Unauthorized' in resp.data
        self.logout()
        resp = self.app.get('/get_last')
        assert 'Unauthorized' in resp.data

    def test_locations(self):
        assert db.session.query(models.Location).count() == 4
        l = models.Location.query.get(2)
        assert 'Bedroom' in l.name
        assert l.sensors.count() == 0

    def register_sensor(self):
        with open('./examples/sensor_example', 'r') as content_file:
            j_sensor = json.load(content_file)

        self.app.post('/register', data=json.dumps(j_sensor))
        sensor = models.Sensor.query.get(1)

        assert sensor.id == 1
        assert j_sensor['name'] in sensor.name
        assert j_sensor['type'] in sensor.type
        assert j_sensor['location'] == sensor.location
        assert sensor.alive == 1
        assert sensor.events.count() == 0

        assert isfile(views.schema_prefix + format_filename(sensor.type) + views.schema_suffix)
        with open(views.schema_prefix + format_filename(sensor.type) + views.schema_suffix, 'r') as content_file:
            assert json.dumps(j_sensor['event_definition']) in content_file.read()

    def keep_alive_sensor(self):
        with open('./examples/sensor_id_example', 'r') as content_file:
            j_sensor = json.load(content_file)

        alive = models.Sensor.query.get(j_sensor['id']).alive
        self.app.post('/keep_alive', data=json.dumps(j_sensor))
        assert models.Sensor.query.get(j_sensor['id']).alive == alive + 1

    def fire_event(self):
        with open('./examples/event_example', 'r') as content_file:
            j_event = json.load(content_file)

        alive = models.Sensor.query.get(j_event['sensor_id']).alive
        self.app.post('/event', data=json.dumps(j_event))
        event = models.Event.query.get(1)

        assert event.id == 1
        assert j_event['timestamp'] == mktime(event.timestamp.timetuple())
        assert j_event['sensor_id'] == event.sensor

        assert models.Sensor.query.get(1).alive == alive + 1

    def unregister_sensor(self):
        with open('./examples/sensor_id_example', 'r') as content_file:
            j_sensor = json.load(content_file)

        sensor_type = models.Sensor.query.get(j_sensor['id']).type
        self.app.post('/unregister', data=json.dumps(j_sensor))

        assert db.session.query(models.Sensor).count() == 0
        assert db.session.query(models.Event).count() > 0

        assert not isfile(views.schema_prefix + format_filename(sensor_type) + views.schema_suffix)

    def not_enough_authorization(self):
        resp = self.app.get('/init')
        assert 'Unauthorized' in resp.data

    def test_sensors(self):
        self.login_logout_authentication()
        self.login()
        self.register_sensor()
        self.keep_alive_sensor()
        self.fire_event()
        self.unregister_sensor()
        self.not_enough_authorization()
        self.logout()

if __name__ == '__main__':
    unittest.main()
