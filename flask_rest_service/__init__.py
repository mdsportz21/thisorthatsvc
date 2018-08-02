#!flask/bin/python
import os

from bson import ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

from bracket import SeedingStrategy
from flask_rest_service.resource import BracketResource
from model import codec
from model.dto import DupesDTO, BracketFieldDTO
from repository import TeamRepository, BracketRepository
from util import to_json

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/thisorthat"

app = Flask(__name__)

with app.app_context():
    app.config['MONGO_URI'] = MONGO_URL
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://damp-ridge-24839.herokuapp.com"]}})
    pymongo = PyMongo(app)
    team_repository = TeamRepository(pymongo)
    bracket_repository = BracketRepository(pymongo)
    bracket_resource = BracketResource(pymongo)


@app.route('/', methods=['GET'])
def test():
    return dumps({
        'status': 'OK',
        'mongo': str(pymongo.db),
    }), 200


# for dev purposes only
@app.route('/api/bracket/field', methods=['POST'])
def create_bracket_field():
    grouping_name = 'MILB'
    team_records = team_repository.get_unique_team_records_by_grouping(grouping_name)

    bracket_field_name = 'MILB'
    bracket_repository.create_bracket_field(bracket_field_name, team_records)
    return dumps({'success': True}), 200


# for dev purposes
# @app.route('/api/import', methods=['POST'])
# def import_teams():
#     team_records = scraper.get_teams_from_files()
#     team_dao.store_team_records(team_records)
#     return dumps({'importSuccessful': True}), 200


# retrieve a list of available brackets
@app.route('/api/bracket', methods=['GET'])
def get_bracket_fields():
    bracket_field_records = bracket_repository.get_all_bracket_field_records()
    bracket_field_dtos = [BracketFieldDTO.from_record(bracket_field_record) for bracket_field_record in
                          bracket_field_records]
    return jsonify(bracketFields=[dto.__dict__ for dto in bracket_field_dtos])


# create a bracket instance
# params include bracket name (required), authenticated user, and seed order (random or by user's previous results)
# raise error if user is not authenticated to create a bracket instance for this user
@app.route('/api/bracket', methods=['POST'])
def create_bracket_instance():
    validate_post(request, ['user', 'seedingStrategy', 'bracketFieldId'])

    # user to create bracket for
    user = request.json['user']

    # random or by user's ranking (if the user has no history, default to random)
    seeding_strategy = SeedingStrategy[request.json['seedingStrategy'].upper()]

    # id of bracket field to create bracket instance from
    bracket_field_id = ObjectId(request.json['bracketFieldId'])

    # generate a new bracket instance
    bracket_instance_response = bracket_resource.create_and_store_bracket_instance(bracket_field_id, seeding_strategy,
                                                                                 user)

    # send response
    return jsonify(bracketInstance=bracket_instance_response.to_dict())


# get a bracket instance by bracket id
# raise error if user is not authenticated to fetch this bracket instance
@app.route('/api/bracket_instance/<name>')
def get_bracket_instance(bracket_instance_id):
    raise NotImplementedError


# save a bracket instance
# params include: bracket name, results
# raise error if user is not authenticated to save this bracket instance
@app.route('/api/bracket_instance/results', methods=['POST'])
def save_bracket_results():
    raise NotImplementedError


# for dev purposes only
@app.route('/api/dupes', methods=['POST'])
def save_dupes():
    validate_post(request, ['teamIds', 'name'])
    name = request.json['name']
    team_ids = [ObjectId(team_id) for team_id in request.json['teamIds']]

    team_repository.save_dupes(name, team_ids)

    # return ok
    return dumps({'resultsSaved': True}), 200


def validate_post(request, required_props):
    # type: (LocalProxy, list[str]) -> None
    if not request.json:
        abort(400, {'message': 'json required in request'})
    for prop in required_props:
        if prop not in request.json:
            abort(400, {'message': '{} required in request'.format(prop)})


# for dev purposes only
@app.route('/api/dupes', methods=['GET'])
def get_dupe_grouping() -> str:
    teams = team_repository.get_group_with_max_count()
    name = teams[0].name if len(teams) > 0 else None
    dupes_dto = DupesDTO(name=name, teams=codec.to_team_dtos(teams))
    return to_json(dupes_dto, 'dupeGroup')


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)
