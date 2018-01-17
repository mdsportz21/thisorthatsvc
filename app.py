#!flask/bin/python
from collections import Iterable

from bson import ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from flask_pymongo import PyMongo

import importer
from bracket import BracketFactory
from db.storage import TeamDAO, SlotDAO, BracketDAO
from model import codec
from model.dto import BracketWrapperDTO
from model.record import TeamRecord, BracketRecord, SlotRecord
from repository import TeamRepository, BracketRepository, SlotRepository
from util import to_dict

app = Flask('thisorthat')
with app.app_context():
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    pymongo = PyMongo(app)
    team_repository = TeamRepository(pymongo)
    bracket_repository = BracketRepository(pymongo)
    slot_repository = SlotRepository(pymongo)
    team_dao = TeamDAO(pymongo)
    slot_dao = SlotDAO(pymongo)
    bracket_dao = BracketDAO(pymongo)


@app.route('/api/bracket/<name>', methods=['GET'])
def get_bracket_json_by_name(name):
    # type: (str) -> str
    team_records = team_repository.get_team_records()
    bracket_record = bracket_repository.get_bracket(name)
    slot_records = slot_repository.get_slots(bracket_record.id)
    return get_bracket_json(team_records, slot_records, bracket_record)


@app.route('/api/import', methods=['POST'])
def import_teams():
    team_records = importer.get_team_records_from_csv('resources/hatz_import_data_final.csv')
    team_records = team_dao.store_team_records(team_records)
    return dumps({'importSuccessful': True}), 200


@app.route('/api/bracket', methods=['POST'])
def generate_bracket():
    if not request.json or 'name' not in request.json:
        abort(400, {'message': 'name required in response'})

    name = request.json['name']

    if bracket_repository.has_bracket(name):
        abort(400, {'message': 'bracket with name {0} already exists'.format(name)})

    team_records = team_repository.get_team_records()
    bracket_id = ObjectId()
    slot_records = BracketFactory.generate_slot_records(team_records, bracket_id)
    slot_records = slot_dao.store_slots(slot_records)
    bracket_record = BracketFactory.generate_bracket(slot_records, bracket_id, name)
    bracket_record = bracket_dao.store_bracket(bracket_record)

    return get_bracket_json(team_records, slot_records, bracket_record)
    # TODO: make sure slot and subject dtos are returned with IDs


def get_bracket_json(team_records, slot_records, bracket_record):
    # type: (list[TeamRecord], list[SlotRecord], BracketRecord) -> str
    bracket_wrapper_dto = BracketWrapperDTO(bracket=codec.to_bracket_dto(bracket_record),
                                            teams=codec.to_team_dtos(team_records, slot_records))
    return to_json(bracket_wrapper_dto, 'bracket')


def to_json(items, name='subjects', other_dict=None):
    # type: (object, str, dict) -> str
    json_items = [to_dict(item) for item in items] if isinstance(items, Iterable) else to_dict(items)
    results = {name: json_items}
    if other_dict is not None:
        results.update(other_dict)
    return dumps(results)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)
