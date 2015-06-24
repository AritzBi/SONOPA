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
MAXPEOPLE_WEIGHT=0.5
SNINTERACTIONS_WEIGHT=0.5
#Controller's user ID for the social network
UID=1
#Social network's
sn_key= "dhT6pd3VGju476BS"
# total number of past days from which threshold for different activities are computed
num_days = 63
# maximum allowed accumulative probability at each end of the distribution to be marked as outlier
prob_sens = 0.1
#Hour for they daily computation
computation_cron = 12

sms_url = 'http://sonopa.c.smartsigns.nl/venuemaster-web-unified/sms/api/'