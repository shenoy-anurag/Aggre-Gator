import datetime
import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api

from web_aggregator.celery_config.celery_worker import make_celery

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['DB_NAME'] = os.environ.get('DB_NAME')

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

JWT_ACCESS_TOKEN_TIMEDELTA = datetime.timedelta(minutes=20)
JWT_REFRESH_TOKEN_TIMEDELTA = datetime.timedelta(hours=6)

app_jwt = JWTManager(app)

mongo = PyMongo(app)

api = Api(app)

CORS(app)

celery_app = make_celery(app)

# BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME')
#
# bucket_client = boto3.client('s3', aws_access_key_id=os.environ['S3_BUCKET_KEY'],
#                              aws_secret_access_key=os.environ['S3_BUCKET_SECRET_ACCESS_KEY'])
#
# import sqlite3
# from flask import g
#
# DATABASE = '/path/to/database.db'
#
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db
#
# @core.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
