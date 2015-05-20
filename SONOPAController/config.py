__author__ = 'hasier'

from os import path
basedir = path.abspath(path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
#Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql://sonopa:sonopa@localhost/sonopa'
SQLALCHEMY_MIGRATE_URI = 'mysql://sonopa:sonopa@localhost/sonopamigrate'
SQLALCHEMY_MIGRATE_PATH = './db_migration'
DB="sonopa"
DB_USER="sonopa"
DB_PASS="sonopa"
#InformationProvider configuration
MAXPEOPLE_WEIGHT=1
SNINTERACTIONS_WEIGHT=0.8
#Controller's user ID for the social network
UID=1
#Social network's
sn_key= "dhT6pd3VGju476BS"