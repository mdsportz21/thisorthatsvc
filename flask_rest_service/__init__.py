#!flask/bin/python

from bson import ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS, cross_origin
from werkzeug.local import LocalProxy

import auth
import bracket

app = Flask(__name__)

with app.app_context():
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://damp-ridge-24839.herokuapp.com"]}})


@app.route('/', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def test():
    return dumps({
        'status': 'OK',
    }), 200


# retrieve a list of available brackets
@app.route('/api/bracket', methods=['GET'])
def get_bracket_fields():
    bracket_fields = bracket.get_all_bracket_fields()
    return jsonify(bracketFields=[bracket_field.to_dict() for bracket_field in bracket_fields])

# create a bracket instance
@app.route('/api/bracket/<bracket_field_id_str>/demo', methods=['POST'])
def generate_random_bracket_instance(bracket_field_id_str: str):
    validate_post(request, ['bracketSize', 'seedingStrategy'])

    # random or by user's ranking (if the user has no history, default to random)
    seeding_strategy = request.json['seedingStrategy']

    # id of bracket field to create bracket instance from
    bracket_field_id = ObjectId(bracket_field_id_str)

    #
    bracket_size = request.json['bracketSize']

    # generate a new bracket instance
    bracket_instance = bracket.generate_bracket_instance(bracket_field_id, seeding_strategy, 'demo', bracket_size)

    # send response
    return jsonify(bracketInstance=bracket_instance.to_dict())


# create and save a bracket instance
# params include bracket name (required), authenticated user, and seed order (random or by user's previous results)
# raise error if user is not authenticated to create a bracket instance for this user
@app.route('/api/bracket/<bracket_field_id_str>/instance', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth.requires_auth
def create_bracket_instance(bracket_field_id_str: str):
    validate_post(request, ['seedingStrategy'])

    # id of bracket field to create bracket instance from
    bracket_field_id = ObjectId(bracket_field_id_str)

    # user to create bracket for
    # user = request.json['user']
    user = auth.get_user()

    # random or by user's ranking (if the user has no history, default to random)
    seeding_strategy = request.json['seedingStrategy']

    # generate a new bracket instance
    bracket_instance = bracket.generate_and_store_bracket_instance(bracket_field_id, seeding_strategy, user)

    # send response
    return jsonify(bracketInstance=bracket_instance.to_dict())


# get a bracket instance by bracket id
# raise error if user is not authenticated to fetch this bracket instance
@app.route('/api/bracket/<bracket_field_id_str>/instance', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth.requires_auth
def get_bracket_instances(bracket_field_id_str: str):
    bracket_field_id = ObjectId(bracket_field_id_str)
    user = auth.get_user()
    bracket_instances = bracket.fetch_bracket_instances(bracket_field_id, user)
    return jsonify(bracketInstances=[bracket_instance.to_dict() for bracket_instance in bracket_instances])


# get a bracket instance by bracket id
# raise error if user is not authenticated to fetch this bracket instance
@app.route('/api/bracket/<bracket_field_id_str>/instance/<bracket_instance_id_str>', methods=['GET'])
def get_bracket_instance(bracket_field_id_str: str, bracket_instance_id_str: str):
    bracket_field_id = ObjectId(bracket_field_id_str)
    bracket_instance_id = ObjectId(bracket_instance_id_str)
    bracket_instance = bracket.fetch_bracket_instance(bracket_field_id, bracket_instance_id)
    return jsonify(bracketInstance=bracket_instance.to_dict())


# save a bracket instance
# params include: bracket name, results
# raise error if user is not authenticated to save this bracket instance
@app.route('/api/bracket/<bracket_field_id_str>/instance/<bracket_instance_id_str>', methods=['POST'])
def save_bracket_results(bracket_field_id_str: str, bracket_instance_id_str: str):
    validate_post(request, ['user', 'seedingStrategy'])
    bracket_field_id = ObjectId(bracket_field_id_str)
    bracket_instance_id = ObjectId(bracket_instance_id_str)

    raise NotImplementedError


# for dev purposes only
# @app.route('/api/dupes', methods=['POST'])
# def save_dupes():
#     validate_post(request, ['teamIds', 'name'])
#     name = request.json['name']
#     team_ids = [ObjectId(team_id) for team_id in request.json['teamIds']]
#
#     team_repository.save_dupes(name, team_ids)
#
#     # return ok
#     return dumps({'resultsSaved': True}), 200


def validate_post(request, required_props):
    # type: (LocalProxy, list[str]) -> None
    if not request.json:
        abort(400, {'message': 'json required in request'})
    for prop in required_props:
        if prop not in request.json:
            abort(400, {'message': '{} required in request'.format(prop)})


# for dev purposes only
# @app.route('/api/dupes', methods=['GET'])
# def get_dupe_grouping() -> str:
#     teams = team_repository.get_group_with_max_count()
#     name = teams[0].name if len(teams) > 0 else None
#     dupes_dto = DupesDTO(name=name, teams=codec.to_team_dtos(teams))
#     return to_json(dupes_dto, 'dupeGroup')


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


@app.errorhandler(auth.AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# for dev purposes only
# @app.route('/api/bracket/field', methods=['POST'])
# def create_bracket_field():
#     grouping_name = 'MILB'
#     team_records = team_repository.get_unique_team_records_by_grouping(grouping_name)
#
#     bracket_field_name = 'MILB'
#     bracket_repository.create_bracket_field(bracket_field_name, team_records)
#     return dumps({'success': True}), 200


# for dev purposes
# @app.route('/api/import', methods=['POST'])
# def import_teams():
#     team_records = scraper.get_teams_from_files()
#     team_dao.store_team_records(team_records)
#     return dumps({'importSuccessful': True}), 200
