#!flask/bin/python
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS

import importer
from chooser.chooser import Chooser
from model import codec
from model.dto import RankingDTO
from model.dto import SubjectDTO
from ranker.ranker import Ranker
from repository.subject_repository import SubjectRepository
from subject_record_dict import SubjectRecordDict
from util import to_dict

app = Flask('thisorthat')
with app.app_context():
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    subject_repository = SubjectRepository(app)


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
    subject_dtos = codec.from_subject_records(subject_records)
    percentage_completed = chooser.get_percentage_completed()
    return to_json(subject_dtos, 'subjects', {'percentCompleted': percentage_completed})


def to_json(items, name='subjects', other_dict=None):
    json_items = [to_dict(item) for item in items]
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
    subject_repository.store_subject_dtos(subject_dtos)

    return dumps({'scrapeSuccessful': True}), 200


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)
