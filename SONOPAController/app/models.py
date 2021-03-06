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


from app import db
from flask_principal import Permission, RoleNeed
from datetime import datetime


class Location(db.Model):
    """Represents the location of a Sensor in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sensors = db.relationship('Sensor', backref='located_in', lazy='dynamic')


class Sensor(db.Model):
    """Represents a sensor in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sensorRef = db.Column(db.String(64))
    type = db.Column(db.String(64))
    last_alive = db.Column(db.DateTime, default=datetime.now())
    location = db.Column(db.Integer, db.ForeignKey('location.id'))
    events = db.relationship('Event', backref='fired_by', lazy='dynamic')


class Event(db.Model):
    """Represents a sensor fired event"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    #sensorRef = db.Column(db.Integer, db.ForeignKey('sensor.sensorRef'))
    value = db.Column(db.Text)


user_role_association = db.Table('user_role', db.Model.metadata,
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                 db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                                 )
"""Association that relates the user and role models"""


class Role(db.Model):
    """Represents the role of a user in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    """Each Permission grants access to each RoleNeed passed"""
    user_permission = Permission(RoleNeed('user'), RoleNeed('admin'))
    admin_permission = Permission(RoleNeed('admin'))


class User(db.Model):
    """Represents a user in the system"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.Text)
    roles = db.relationship('Role',
                            secondary=user_role_association,
                            backref='users')

    def is_authenticated(self):
        """Method required for the flask_login module"""
        return True

    def is_active(self):
        """Method required for the flask_login module"""
        return True

    def is_anonymous(self):
        """Method required for the flask_login module"""
        return False

    def get_id(self):
        """Method required for the flask_login module"""
        return self.id


class ActivityAnomaly(db.Model):
    """Represents that a given activity has provoked an anomaly in the system"""
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), primary_key=True)
    anomaly_id = db.Column(db.Integer, db.ForeignKey('anomaly.id'), primary_key=True)
    timestamp = db.Column(db.DateTime)
    anomaly = db.relationship('Anomaly', backref='anomaly')


class ActivityModel(db.Model):
    """Represents the model of the different activities that can be inferred in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    activities = db.relationship('Activity', backref='is_a', lazy='dynamic')


class Activity(db.Model):
    """Represents an inferred activity in the behavior model"""
    id = db.Column(db.Integer, primary_key=True)
    activity_model_id = db.Column(db.Integer, db.ForeignKey('activity_model.id'))
    timestamp = db.Column(db.DateTime)
    anomalies = db.relationship('ActivityAnomaly', backref='activity')


class Anomaly(db.Model):
    """Represents the model of the different anomalies that can be fired in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    @staticmethod
    def from_chain_model(anomaly):
        """Returns a database-compatible Anomaly object from the provided Anomaly from the behavior model"""
        activity = Activity.query.get(anomaly.activity_id)
        if activity is None:
            raise ValueError('Activity with id {0} does not exist'.format(anomaly.activity_id))
        a = Anomaly.query.get(anomaly.id)
        if a is None:
            raise ValueError('Anomaly with id {0} does not exist'.format(anomaly.id))
        rel = ActivityAnomaly(timestamp=anomaly.timestamp)
        rel.anomaly = a
        activity.anomalies.append(rel)

        return rel