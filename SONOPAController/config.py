__author__ = 'hasier'

from os import path
basedir = path.abspath(path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'mysql://sonopa:sonopa@localhost/sonopa'
SQLALCHEMY_MIGRATE_URI = 'mysql://sonopa:sonopa@localhost/sonopamigrate'
SQLALCHEMY_MIGRATE_PATH = './db_migration'