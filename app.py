#!flask/bin/python
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS
from flask_pymongo import PyMongo

import importer
from bracket import BracketFactory
from chooser.chooser import Chooser
from model import codec
from model.dto import RankingDTO
from model.dto import SubjectDTO
from ranker import Ranker
from repository import SubjectRepository, BracketRepository
from subject_record_dict import SubjectRecordDict
from util import to_dict
from collections import Iterable

app = Flask('thisorthat')
with app.app_context():
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    pymongo = PyMongo(app)
    subject_repository = SubjectRepository(pymongo)
    bracket_repository = BracketRepository(pymongo)


@app.route('/api/ranking', methods=['GET'])
def get_ranking():
    subject_record_dict = SubjectRecordDict(subject_repository)
    ranker = Ranker(subject_record_dict)
    ranked_subject_records = ranker.get_rankings()
    ranking_dtos = [RankingDTO.to_ranking_dto(subject_record, rank + 1) for rank, subject_record in
                    enumerate(ranked_subject_records)]
    ranker.fill_wins_and_faced(ranking_dtos)
    return to_json(ranking_dtos, 'rankings')


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subject_record_dict = SubjectRecordDict(subject_repository)
    ranker = Ranker(subject_record_dict)
    chooser = Chooser(subject_record_dict, ranker)
    subject_records = chooser.choose()
    subject_dtos = codec.to_subject_dtos(subject_records)
    percentage_completed = chooser.get_percentage_completed()
    return to_json(subject_dtos, 'subjects', {'percentCompleted': percentage_completed})


@app.route('/api/bracket/<name>', methods=['GET'])
def get_bracket(name):
    # type: (str) -> str
    bracket = bracket_repository.get_bracket(name)
    bracket_dto = codec.to_bracket_dto(bracket)
    return to_json(bracket_dto, 'bracket')


def to_json(items, name='subjects', other_dict=None):
    # type: (object, str, dict) -> str
    json_items = [to_dict(item) for item in items] if isinstance(items, Iterable) else to_dict(items)
    results = {name: json_items}
    if other_dict is not None:
        results.update(other_dict)
    return dumps(results)


@app.route('/api/subjects', methods=['POST'])
def save_subject_selection():
    # validate and extract
    if not request.json or 'subjects' not in request.json:
        abort(400, {'message': 'subjects required in response'})
    print "###", request.json, "###"
    subject_dtos = request.json['subjects']
    if len(subject_dtos) < 2:
        abort(400, {'message': 'at least two subjects required in response'})
    for subject in subject_dtos:
        if 'selected' not in subject:
            abort(400, {'message': 'selected required in each subject'})

    # save
    subject_repository.save_choice([SubjectDTO.subject_dto_factory(subject_dto) for subject_dto in subject_dtos])

    return dumps({'responseSaved': True}), 200


@app.route('/api/import', methods=['POST'])
def import_subjects():
    subject_dtos = importer.get_subject_dtos_from_csv('resources/hatz_import_data_final.csv')

    # Old: store in subjects collection
    # subject_repository.store_subject_dtos(subject_dtos)
    # New: store in bracket

    bracket = BracketFactory.generate_bracket_from_dtos(subject_dtos, 'MiLB Hats')
    bracket_repository.store_bracket(bracket)
    return dumps({'scrapeSuccessful': True}), 200


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)
