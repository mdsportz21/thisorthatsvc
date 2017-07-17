#!flask/bin/python
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS

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
    return to_json(ranking_dtos, 'rankings')


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subject_record_dict = SubjectRecordDict(subject_repository)
    chooser = Chooser(subject_record_dict)
    subject_records = chooser.choose()
    subject_dtos = codec.from_subject_records(subject_records)
    return to_json(subject_dtos)


def to_json(items, name='subjects'):
    json_items = [to_dict(item) for item in items]
    return dumps({name: json_items})


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


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)

    # with app.app_context():
    # # Test insert:
    # test_subject_dtos = [
    #     SubjectDTO(imgDesc="Charleston River Dogs", description="Charleston River Dogs", imgLink="https://static1.squarespace.com/static/594061048419c282ed731d4a/5949b25b86e6c05c7d5cf26d/5949b27f6b8f5bfb66cee7e1/1498002048239/thumb+%2814%29.jpeg?format=1500w"),
    #     SubjectDTO(imgDesc="Augusta Greenjackets", description="Augusta Greenjackets", imgLink="https://static1.squarespace.com/static/594061048419c282ed731d4a/59420b38893fc0f697291aa6/59420c2cb3db2bab436210dc/1497500717718/thumb.jpeg?format=1500w"),
    #     SubjectDTO(imgDesc="Biloxi Shuckers", description="Biloxi Shuckers", imgLink="https://static1.squarespace.com/static/594061048419c282ed731d4a/5942ff9f3e00be915c807ade/59443fdb17bffcdd0ef9e6fe/1497645020298/thumb+%282%29.jpeg?format=2500w"),
    #     SubjectDTO(imgDesc="Burlington Bees", description="Burlington Bees", imgLink="https://static1.squarespace.com/static/594061048419c282ed731d4a/59496f1fdb29d6f4e5731f2d/59496f3d414fb5804d2dab58/1497984834262/thumb+%2810%29.jpeg?format=2500w")
    # ]
    # subject_repository.store_subject_dtos(test_subject_dtos)

    # # Test fetch
    # subjects = subject_repository.get_subject_records()
    # print SubjectRecord.subject_record_factory(subjects[0])
