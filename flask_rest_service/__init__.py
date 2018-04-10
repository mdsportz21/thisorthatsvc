import os
from flask import Flask, make_response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_restful import Api

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj))
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import flask_rest_service.resources