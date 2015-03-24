__author__ = 'hasier'

import sys,os
#sys.path.insert(0, os.path.realpath('..'))
#sys.path.insert(0, os.path.join( os.path.realpath('..'),'TimeMarkov'))
#sys.path.insert(0, os.path.join( os.path.realpath('..'),'TimeMarkov/controller_api.py'))
from jsonschema.exceptions import ValidationError
from app import db, models, app, login_manager
from flask import request, g, redirect, url_for, render_template, flash
from app.database import db_create
from datetime import datetime, timedelta
import calendar
from calendar import timegm
import json
from jsonschema import validate
from os import remove
from os.path import isfile
from utils import format_filename, check_pass, hash_pass, get_timestamp
import socket
from time import sleep, mktime
from app.decorators import async
from flask_login import login_user, logout_user, session, current_user, login_required
from flask_principal import identity_changed, Identity, AnonymousIdentity, identity_loaded, RoleNeed, UserNeed
#import TimeMarkov.controller_api
from activity_inference import Reasoner
from json import JSONEncoder
import requests


schema_prefix = './app/schemas/'
schema_suffix = '_schema'
sensor_schema = schema_prefix + 'register_sensor_schema'
unregister_sensor_schema = schema_prefix + 'unregister_sensor_schema'
event_schema = schema_prefix + 'event_schema'
keep_alive_schema = schema_prefix + 'keep_alive_sensor_schema'
keep_alive_list_schema = schema_prefix + 'keep_alive_list_schema'
configuration_file = './app/configuration/config.json'

#model_backup_file = './model_backup/model.bak'

sensor_cleanup_rounds = 3
sensor_cleanup_round_time = 600
last_allowed_alive = None

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 10000

config = None
model = None
reasoner = Reasoner()
started = False


@app.route('/')
def index():
    return "Hello from SONOPA controller!"


@app.route('/init')
def init():
    """GET call that initializes the database and the different underlying systems"""
    with open(configuration_file, 'r') as f:
        global config
        config = json.load(f)
        global last_allowed_alive
        last_allowed_alive = timedelta(seconds=int(config['last_allowed_alive']))

    message = init_db()

    if not app.config['TESTING'] and not started:
        global started
        started = True
        global model
        _cron()

    return message

def init_db():
    """Initializes the database if needed"""

    if db.engine.dialect.has_table(db.session, 'location'):
        message = 'Controller already initialized'
    else:
        print 'Initializing database...'
        db_create.init_db()
        l = models.Location(name='Kitchen')
        db.session.add(l)
        db.session.commit()

        l = models.Location(name='Bedroom')
        db.session.add(l)
        db.session.commit()

        l = models.Location(name='Bathroom')
        db.session.add(l)
        db.session.commit()

        l = models.Location(name='Living room')
        db.session.add(l)
        db.session.commit()

        r = models.Role(name='user')
        db.session.add(r)
        db.session.commit()

        u = models.User(username='user', pw_hash=hash_pass('user'))
        db.session.add(u)
        db.session.commit()

        u.roles.append(r)
        db.session.commit()

        r = models.Role(name='admin')
        db.session.add(r)
        db.session.commit()

        a = models.ActivityModel(name='Wake')
        db.session.add(a)
        db.session.commit()

        a = models.ActivityModel(name='Cook')
        db.session.add(a)
        db.session.commit()

        a = models.ActivityModel(name='Relax')
        db.session.add(a)
        db.session.commit()

        a = models.ActivityModel(name='Eat')
        db.session.add(a)
        db.session.commit()

        a = models.ActivityModel(name='Sleep')
        db.session.add(a)
        db.session.commit()

        message = 'Controller correctly initialized'

    return message


def _cron():
    """Initializes the different scheduled tasks"""
    _cleanup_cron()
    #if app.config['UPDATE-SOCIAL-NETWORK']:
        #_send_model_update_cron()
    #_exit_training_cron()
    #_backup_cron()
    if app.config['FAKE-SENSORS']:
        _fake_sensors_cron()


@async
def _fake_sensors_cron():
    """Sends every 0-100 seconds a new fake sensor event"""
    sleep(10)
    print 'Logging in for fake sensors'
    r = requests.post('http://localhost:5000/login', data={'username': 'user', 'password': 'user'})
    cookie = r.headers['Set-Cookie']
    cookie = cookie[:cookie.index(';')]
    headers = {'Cookie': cookie}

    print 'Login complete. Registering sensors'
    with open('./examples/sensor_example', 'r') as f:
        j = json.load(f)
    r = requests.post('http://localhost:5000/register', data=json.dumps(j), headers=headers)
    temp_id = int(r.text)
    j['name'] = 'Humidity'
    j['type'] = 'SHT21'
    j['location'] = "Kitchen"
    j['sensorRef']="cronGeneratedSensor"
    r = requests.post('http://localhost:5000/register', data=json.dumps(j), headers=headers)
    hum_id = int(r.text)
    with open('./examples/sensor2_example', 'r') as f:
        j = json.load(f)
    r = requests.post('http://localhost:5000/register', data=json.dumps(j), headers=headers)
    keep_alive_id = int(r.text)
    with open('./examples/sensor3_example', 'r') as f:
        j = json.load(f)
    r = requests.post('http://localhost:5000/register', data=json.dumps(j), headers=headers)
    print 'Registration complete. Generating random data'
    from random import random, randrange
    while True:
        sleep(int(random() * 100))
        if random() < 0.5:
            temp = randrange(15, 30, 1)
            if random() < 0.5:
                temp += 0.5
            temp = float(temp)
            print 'New temperature sensor event, value: ' + str(temp)
            send = {'timestamp': get_timestamp(), 'sensor_id': temp_id, 'value': {'value': temp}}
            print 'Response: ' + requests.post('http://localhost:5000/event', data=json.dumps(send),
                                               headers=headers).text
        else:
            hum = randrange(40, 95, 1)
            send = {'timestamp': get_timestamp(), 'sensor_id': hum_id, 'value': {'value': hum}}
            print 'New humidity sensor event, value: ' + str(hum)
            print 'Response: ' + requests.post('http://localhost:5000/event', data=json.dumps(send),
                                               headers=headers).text
        if random()<0.3:
            print 'New keep alive message for sensor' + str(keep_alive_id)
            send={'id':keep_alive_id}
            print 'Response: '+requests.post("http://localhost:5000/keep_alive", data=json.dumps(send),headers=headers).text


"""@async
def _backup_cron():
    #Schedules a new model backup
    while True:
        sleep(60)  # TODO Setup larger backup interval
        print 'Backup model to ' + model_backup_file
        model.backup(model_backup_file)


@async
def _exit_training_cron():
    #Exits the training mode of the behavior model
    sleep(2592000)
    model.exit_training()


@async
def _send_model_update_cron():
    #Schedules a periodical update of the model to the social network
    while True:
        url = 'http://www.sonopa.com/network/model'  # TODO Set correct URL
        response = _send_post(url, model.get_serialized_model)  # TODO Handle response
        sleep(21600)  # Send four times per day"""


@async
def _cleanup_cron():
    """Schedules a periodical cleanup of the sensors that do not seem to be alive"""
    rounds = int(int(config['keep_alive_round']) / sensor_cleanup_round_time)
    while True:
        print 'Waiting for discoveries...'
        for i in range(rounds):
            _discovery()
            sleep(sensor_cleanup_round_time)

        print 'Cleaning sensors...'

        i = 0
        print datetime.now() - last_allowed_alive
        sensors = db.session.query(models.Sensor).filter(
            (models.Sensor.last_alive) < datetime.now() - last_allowed_alive).all()
        for sensor in sensors:
            _remove_sensor(sensor)
            i += 1
        """sensors = db.session.query(models.Sensor).all()
        for sensor in sensors:
            if((datetime.now() - sensor.last_alive)>last_allowed_alive):
                _remove_sensor(sensor)
                i += 1"""
        print '{0} sensors cleaned'.format(i)

        i = 0
        sensors = db.session.query(models.Sensor).all()
        for sensor in sensors:
            sensor.last_alive = datetime.now()
            i += 1
        print '{0} sensors kept alive'.format(i)

        db.session.commit()


sending = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
"""Socket to send the BROADCAST messages"""
sending.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)


def _discovery():
    """Sends a sensor discovery broadcast message"""
    sending.sendto("Discovery", (MCAST_GRP, MCAST_PORT))


@login_manager.user_loader
def load_user(user_id):
    """Method required for the flask_login module"""
    return models.User.query.get(user_id)


@app.before_request
def before_request():
    """Before each request adds to the special variable g the current user,
    so that it is available in the Jinja2 templates"""
    g.user = current_user


@app.context_processor
def utility_processor():
    """Preprocessor to make available custom methods in Jinja2 templates"""
    return dict(min=min, int=int)


@app.route('/login', methods=['GET'])
def show_login():
    """Displays the login page to the user, if not authenticated"""
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('get_sensors'))
    session['is_html'] = True
    return render_template('login.html', title='Sign In')


@app.route('/login', methods=['POST'])
def login():
    """Logs in a user into the system. The POST call must provide the correct credentials
    in application/x-www-form-urlencoded format"""
    user = db.session.query(models.User).filter(models.User.username == request.form['username']).first()

    if not user is None and check_pass(request.form['password'], user.pw_hash):
        login_user(user)

        # Tell Flask-Principal the identity changed
        identity_changed.send(app, identity=Identity(user.id))

        if 'is_html' in session and session['is_html']:
            return redirect(url_for('get_sensors'))
        return 'Welcome {0}!'.format(user.username)
    else:
        if session['is_html']:
            flash('Invalid login. Please try again.')
            return redirect(url_for('login'))
        return 'Login unsuccessful'


@app.route('/logout')
@login_required
def logout():
    """The current user session is terminated"""
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    if session['is_html']:
        return redirect(url_for('login'))
    return 'Bye!'


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """Assigns permissions to the current user according to its role.
    Required by flask_principal module"""
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Update the identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))


@app.route('/sensors')
@login_required
@models.Role.user_permission.require(http_exception=401)
def get_sensors():
    """Displays all the sensors registered in the system"""
    sensors = models.Sensor.query.all()
    return render_template('sensors.html', sensors=sensors)


@app.route('/sensors/<int:sensor>')
@login_required
@models.Role.user_permission.require(http_exception=401)
def get_events(sensor):
    """Displays all the events registered in the system for the given sensor"""
    s = models.Sensor.query.get(sensor)
    list=s.events.all()
    cols = ['id', 'timestamp', 'value']
    #Get only the information of the column specified in cols
    list = [{col: getattr(d, col) for col in cols} for d in list]
    current_time = datetime.utcnow()
    #Get the events of the last 24 hours
    week_ago = current_time - timedelta(days=1)
    lastWeekEvents = s.events.filter(models.Event.timestamp >week_ago).all()
    lastWeekEvents = [{col: getattr(d, col) for col in cols} for d in lastWeekEvents]
    return render_template('events.html', events=s.events.all(), sensor=s,eventsJS=json.dumps(list,cls=MyEncoder),lastWeekEventsJS=json.dumps(lastWeekEvents,cls=MyEncoder))


@app.route('/keep_alive', methods=['POST'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def keep_alive():
    """Sets the given sensor as alive if the provided JSON POST message is correctly formed"""
    try:
        sensor = json.loads(request.data)
        with open(keep_alive_schema, 'r') as f:
            validate(sensor, json.load(f))
    except ValueError as e:
        return 'JSON data is malformed: {0}'.format(e.message)
    except ValidationError as e:
        return 'JSON does not comply with schema: {0}'.format(e.message)
    else:
        sensor_id = sensor['id']

        s = models.Sensor.query.get(sensor_id)
        if s is None:
            return 'Invalid sensor id: {0}'.format(sensor_id)
        else:
            s.last_alive = datetime.now()
            db.session.commit()

            return "Sensor alive: {0}<br />".format(sensor_id)
@app.route('/keep_alive_list', methods=['POST'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def keep_alive_list():
    """Sets the given list of sensors as alive if the provided JSON POST message is correctly formed"""
    try:
        sensor_list = json.loads(request.data)
        with open(keep_alive_list_schema, 'r') as f:
            validate(sensor_list, json.load(f))
    except ValueError as e:
        return 'JSON data is malformed: {0}'.format(e.message)
    except ValidationError as e:
        return 'JSON does not comply with schema: {0}'.format(e.message)
    else:
        return_message=""
        for sensor_id in sensor_list:
            s = models.Sensor.query.get(sensor_id)
            if s is None:
                return_message=return_message+'Invalid sensor id: {0}'.format(sensor_id)
            else:
                s.last_alive = datetime.now()
                db.session.commit()
                return_message=return_message+  " Sensor alive: {0}<br />".format(sensor_id)
        return return_message

@app.route('/register', methods=['POST'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def register_sensor():
    """Registers given sensor in the system if the provided JSON POST message is correctly formed.
    An id is assigned to it and is returned"""
    try:
        sensor = json.loads(request.data)
        with open(sensor_schema, 'r') as f:
            validate(sensor, json.load(f))
    except ValueError as e:
        return 'JSON data is malformed: {0}'.format(e.message)
    except ValidationError as e:
        return 'JSON does not comply with schema: {0}'.format(e.message)
    else:
        name = sensor['name']
        sensor_type = sensor['type']
        #location_id = sensor['location']
        location_name=sensor['location']
        #l = models.Location.query.get(location_id)
        l=models.Location.query.filter_by(name=location_name).all()
        if len(l) == 0:
            l=models.Location(name=location_name)
            db.session.add(l)
            db.session.commit()
            if 'sensorRef' in sensor:
                s = models.Sensor(name=name, type=sensor_type, located_in=l,sensorRef=sensor['sensorRef'])
            else:
                s = models.Sensor(name=name, type=sensor_type, located_in=l)
            db.session.add(s)
            db.session.commit()
            if not isfile(schema_prefix + format_filename(sensor_type) + schema_suffix):
                with open(schema_prefix + format_filename(sensor_type) + schema_suffix, 'w+') as f:
                    json.dump(sensor['event_definition'], f)

            return "{0}".format(s.id)

        else:
            if 'sensorRef' in sensor:
                s = models.Sensor(name=name, type=sensor_type, located_in=l[0],sensorRef=sensor['sensorRef'])
            else:
                s = models.Sensor(name=name, type=sensor_type, located_in=l[0])
            db.session.add(s)
            db.session.commit()

            if not isfile(schema_prefix + format_filename(sensor_type) + schema_suffix):
                with open(schema_prefix + format_filename(sensor_type) + schema_suffix, 'w+') as f:
                    json.dump(sensor['event_definition'], f)

            return "{0}".format(s.id)
        #Previous way, giving the ID.
        """if l is None:
            return 'Invalid location id: {0}'.format(location_id)
        else:
            s = models.Sensor(name=name, type=sensor_type, located_in=l)
            db.session.add(s)
            db.session.commit()

            if not isfile(schema_prefix + format_filename(sensor_type) + schema_suffix):
                with open(schema_prefix + format_filename(sensor_type) + schema_suffix, 'w+') as f:
                    json.dump(sensor['event_definition'], f)

            return "{0}".format(s.id)"""


@app.route('/unregister', methods=['POST'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def unregister_sensor():
    """Unregisters the given sensor if the provided JSON POST message is correctly formed"""
    try:
        sensor = json.loads(request.data)
        with open(unregister_sensor_schema, 'r') as f:
            validate(sensor, json.load(f))
    except ValueError as e:
        return 'JSON data is malformed: {0}'.format(e.message)
    except ValidationError as e:
        return 'JSON does not comply with schema: {0}'.format(e.message)
    else:
        sensor_id = sensor['id']

        s = models.Sensor.query.get(sensor_id)
        if s is None:
            return 'Invalid sensor id: {0}'.format(sensor_id)
        else:
            _remove_sensor(s)

            return "{0}".format(sensor_id)


def _remove_sensor(sensor):
    """Removes the given sensor from the system"""
    sensor_type = sensor.type
    db.session.delete(sensor)
    db.session.commit()

    remaining = db.session.query(models.Sensor).filter(models.Sensor.type == sensor_type).count()

    if remaining == 0:
        remove(schema_prefix + format_filename(sensor_type) + schema_suffix)


@app.route('/event', methods=['POST'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def on_event():
    """Saves the given event from a sensor if the provided JSON POST message is correctly formed"""
    try:
        event = json.loads(request.data)
        print event
        with open(event_schema, 'r') as f:
            validate(event, json.load(f))
    except ValueError as e:
        return 'JSON data is malformed: {0}'.format(e.message)
    except ValidationError as e:
        return 'JSON does not comply with schema: {0}'.format(e.message)
    else:
        timestamp = int(event['timestamp'] / 1000)
        value = event['value']
        value=json.dumps(value)
        sensor_id = event['sensor_id']
        s = models.Sensor.query.get(sensor_id)
        if s is None:
            return 'Invalid sensor id: {0}'.format(sensor_id)
        else:
            s.last_alive = datetime.now()
            try:
                with open(schema_prefix + format_filename(s.type) + schema_suffix, 'r') as f:
                    validate(event['value'], json.load(f))
            except ValidationError as e:
                return 'JSON does not comply with schema: {0}'.format(e.message)
            else:
                e = models.Event(timestamp=datetime.fromtimestamp(timestamp), fired_by=s, value=str(value))
                db.session.add(e)
                db.session.commit()

                #_append_sensor_event(e)

                return "{0}".format(e.id)
@app.route('/api/list_sensors',methods=['GET'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def on_api_list_sensors():
    """Returns the list of all the sensors in the system: type, location_name, sensor_id"""
    sensors=models.Sensor.query.all()
    json_str='['
    i=0
    for sensor in sensors:
        if i==0:
            json_str+='{"sensor_id": "%s", "name": "%s", "type": "%s", "location": "%s","sensorRef":"%s"}' % (sensor.id,sensor.name,sensor.type,models.Location.query.get(sensor.location).name,sensor.sensorRef)
        else:
            json_str+=',{"sensor_id": "%s", "name": "%s", "type": "%s", "location": "%s","sensorRef":"%s"}' % (sensor.id,sensor.name,sensor.type,models.Location.query.get(sensor.location).name,sensor.sensorRef)
        i+=1
    json_str+=']'
    return json_str

@app.route('/api/sensors/<int:sensor>',methods=['GET'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def on_api_sensor(sensor):
    s = models.Sensor.query.get(sensor)
    if s is None:
            return 'Invalid sensor id: {0}'.format(sensor)
    else:
        list=s.events.all()
        for l in list:
            tt = datetime.timetuple(l.timestamp)
            sec_epoch_utc = calendar.timegm(tt)
            l.timestamp=int(sec_epoch_utc)
        cols = ['id', 'timestamp', 'value']
        #Get only the information of the column specified in cols
        list = [{col: getattr(d, col) for col in cols} for d in list]
        eventsJS=json.dumps(list,cls=MyEncoder)
        return eventsJS

@app.route('/api/sensors/<int:sensor>/<int:start>/<int:end>',methods=['GET'])
@login_required
@models.Role.user_permission.require(http_exception=401)
def on_api_sensor_interval(sensor,start=1,end=1):
    s = models.Sensor.query.get(sensor)
    if s is None:
        return 'Invalid sensor id: {0}'.format(sensor)
    else:
        start=datetime.fromtimestamp(start)
        end=datetime.fromtimestamp(end)
        cols = ['id', 'timestamp', 'value']
        events = s.events.filter(models.Event.timestamp >start).filter(models.Event.timestamp<end).all()
        for event in events:
            tt = datetime.timetuple(event.timestamp)
            sec_epoch_utc = calendar.timegm(tt)
            event.timestamp=int(sec_epoch_utc)            
        events = [{col: getattr(d, col) for col in cols} for d in events]
        eventsJS=json.dumps(events,cls=MyEncoder)
        return eventsJS
@async
def _append_sensor_event(event):
    """Collects the given sensor event. Then, if an activity is inferred,
    anomalies are checked and the social network is updated"""
    print 'Reasoning activities from sensor events'
    reasoner.feed(event)
    activity = reasoner.infer_activity()

    if not activity is None:
        print 'Sensor data generated a new activity: ' + activity.is_a.name
        anomaly = model.check_anomaly(activity.is_a.name)

        if anomaly is None:
            # If new activity inferred and no anomaly detected, send it to the social network
            print 'No anomaly detected, storing data and sending to social network'

            model.new_sensor_event(activity.is_a.name, activity.timestamp)

            db.session.add(activity)
            db.session.commit()

            if app.config['UPDATE-SOCIAL-NETWORK']:
                url = 'http://www.sonopa.com/network/newactivity'  # TODO Set correct URL
                json_obj = dict()
                json_obj['user_id'] = config['id']
                json_obj['activity'] = {'id': activity.is_a.id, 'name': activity.is_a.name}
                json_obj['timestamp'] = get_timestamp(mktime(activity.timestamp.timetuple()))
                # response = _send_json_post(url, json_obj)  # TODO Uncomment and handle response
        else:
            print 'Anomaly detected, sending alert to social network'
            try:
                db.session.add(models.Anomaly.from_chain_model(anomaly))
            except ValueError as e:
                print e.message
            else:
                db.session.commit()

                if app.config['UPDATE-SOCIAL-NETWORK']:
                    url = 'http://www.sonopa.com/network/anomaly'  # TODO Set correct URL
                    json_obj = dict()
                    json_obj['user_id'] = config['id']
                    json_obj['activity'] = {'id': anomaly.activity_id, 'name': anomaly.activity_name}
                    json_obj['timestamp'] = get_timestamp(mktime(anomaly.timestamp.timetuple()))
                    json_obj['anomaly_id'] = anomaly.id
                    # response = _send_json_post(url, json_obj)  # TODO Uncomment and handle response


def _send_json_post(url, json_obj):
    """Sends the given JSON object to the given URL"""
    return _send_post(url, json.dumps(json_obj), {'Content-Type': 'application/json'})


def _send_post(url, data, headers=None):
    """Sends the given data to the given URL via POST messsage"""
    return requests.post(url, data=data, headers=headers).text


@app.route('/get_last')
@login_required
@models.Role.user_permission.require(http_exception=401)
def get_last_event():
    """Returns the details of the last event in the system"""
    e = db.session.query(models.Event).order_by(models.Event.id.desc()).first()
    if e is None:
        return 'No events stored'
    else:
        return 'Last event ({0}) {1} activated in the {2} and sent value: {3}'.format(e.timestamp,
                                                                                      e.fired_by.name,
                                                                                      e.fired_by.located_in.name,
                                                                                      e.value)

@app.route('/rules', methods=['GET'])
def rules():
    sensors=models.Sensor.query.all()
    sensor_types=db.session.query(models.Sensor.type).distinct()
    activity_types=db.session.query(models.ActivityModel.name).distinct()
    with open('rules.json', 'r') as f:
        rules = json.load(f)
    return render_template('rules.html',rules=rules, sensors=sensors, sensors_types=sensor_types, activity_types=activity_types, title='Rule system')

@app.route('/get_sensors_by_type', methods=['GET'])
def get_sensors_by_type():
    sensor_type = request.args.get('sensor_type', 0, type=str)
    sensors = models.Sensor.query.filter_by(type=sensor_type)
    data=[]
    for sensor in sensors:
        data_sensor=dbToJSon(sensor)
        if data_sensor != -1: 
            data.append(data_sensor)
    return json.dumps(data)

@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    sensor_id = request.args.get('sensor_id', 0, type=int)
    s = models.Sensor.query.get(sensor_id)
    print s.type
    data=dbToJSon(s)
    return json.dumps(data)
@app.route('/set_rules', methods=['POST'])
def set_rules():
    data = json.loads(request.data)
    print data
    with open('rules.json', 'w') as outfile:
        json.dump(data, outfile)
    return "OK"

def dbToJSon(sensor):
    sensor_type=sensor.type
    print sensor_type
    print sensor.id
    if sensor_type=="TMP36" or  sensor_type=="SHT21" :
        max=0
        min=sys.maxint
        avg=0
        i=0
        for event in sensor.events:
            data=event.value
            data=json.loads(data)
            data=float(data['value'])
            if max<data:
                max=data
            if min>data:
                min=data
            avg=avg+data
            i=i+1
        if i!=0:
            avg=avg/i
            avg="%.2f" % avg
            return {'sensor_id': sensor.id, 'location':models.Location.query.get(sensor.location).name ,'max':max,'min':min,'avg':avg}
        else: 
            return -1
         

# @app.errorhandler(404)
# def internal_error(error):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500

#Encoder to send events data in json
class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =obj.__dict__
        return encoded_object
