#!flask/bin/python

__author__ = 'hasier'

from migrate.versioning import api
from app import app, db
from os.path import exists


def init_db():
    """Initializes the database and, if needed, the version control for it"""
    db.create_all()
    if 'SQLALCHEMY_MIGRATE_URI' in app.config:
        if not exists(app.config['SQLALCHEMY_MIGRATE_PATH']):
            api.create(app.config['SQLALCHEMY_MIGRATE_PATH'], 'database repository')
            api.version_control(app.config['SQLALCHEMY_MIGRATE_URI'], app.config['SQLALCHEMY_MIGRATE_PATH'])
        else:
            api.version_control(app.config['SQLALCHEMY_MIGRATE_URI'], app.config['SQLALCHEMY_MIGRATE_PATH'],
                                api.version(app.config['SQLALCHEMY_MIGRATE_PATH']))


if __name__ == '__main__':
    init_db()