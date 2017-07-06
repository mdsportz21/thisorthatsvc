#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS, cross_origin
from chooser import chooser

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

subjects_data = [
    {
      "id": 1,
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/5949b25b86e6c05c7d5cf26d/5949b27f6b8f5bfb66cee7e1/1498002048239/thumb+%2814%29.jpeg?format=1500w",
      "imgDesc": "Charleston River Dogs",
      "description": "C-Town River Dogs"
    },
    {
      "id": 2,
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/59420b38893fc0f697291aa6/59420c2cb3db2bab436210dc/1497500717718/thumb.jpeg?format=1500w",
      "imgDesc": "Augusta Greenjackets",
      "description": "Augusta Greenjackets"
    },
    {
      "id": 3,
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/5942ff9f3e00be915c807ade/59443fdb17bffcdd0ef9e6fe/1497645020298/thumb+%282%29.jpeg?format=2500w",
      "imgDesc": "Biloxi Shuckers",
      "description": "Biloxi Shuckers"
    },
    {
      "id": 4,
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/59496f1fdb29d6f4e5731f2d/59496f3d414fb5804d2dab58/1497984834262/thumb+%2810%29.jpeg?format=2500w",
      "imgDesc": "Burlington Bees",
      "description": "Burlington Bees"
    }
]

my_chooser = chooser.Chooser(subjects_data)


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    result = my_chooser.choose()
    return jsonify({'subjects': result})


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

    return jsonify({'responseSaved': True}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}), 400)


if __name__ == '__main__':
    app.run(debug=True)