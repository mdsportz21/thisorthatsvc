#!flask/bin/python
from bson.json_util import dumps
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS
from flask_pymongo import PyMongo

from chooser import chooser
from db.subject_storage import SubjectDAO

app = Flask('thisorthat')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

mongo = PyMongo(app)
subject_dao = SubjectDAO(mongo)


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subjects_data = subject_dao.get_subjects()
    my_chooser = chooser.Chooser(subjects_data)
    result = my_chooser.choose()
    return dumps({'subjects': result})


@app.route('/api/subjects', methods=['POST'])
def save_subject_selection():
    if not request.json or 'subjects' not in request.json:
        abort(400, {'message': 'subjects required in response'})
    print "###", request.json, "###"
    subjects = request.json['subjects']
    if len(subjects) < 2:
        abort(400, {'message': 'at least two subjects required in response'})
    for subject in subjects:
        if 'selected' not in subject:
            abort(400, {'message': 'selected required in each subject'})

    return dumps({'responseSaved': True}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)

# Test insert:
# with app.app_context():
#     subject_dao.store_subjects(subjects_data)
