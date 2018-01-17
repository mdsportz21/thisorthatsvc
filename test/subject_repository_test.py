from bson import ObjectId
from mock import patch

from model.dto import SubjectDTO
from model.record import SubjectRecord
from repository import TeamRepository

subject_ids = {
    'a': ObjectId(24 * 'a'),
    'b': ObjectId(24 * 'b'),
    'c': ObjectId(24 * 'c'),
    'd': ObjectId(24 * 'd'),
    'e': ObjectId(24 * 'e'),
    'f': ObjectId(24 * 'f')
}

subject_dict = {
    subject_ids['a']: {
        '_id': subject_ids['a'],
        '_victims': [
            {'_victim_id': subject_ids['b'], '_explicit': True},
            {'_victim_id': subject_ids['c'], '_explicit': False},
            {'_victim_id': subject_ids['d'], '_explicit': False}
        ]
    },
    subject_ids['b']: {
        '_id': subject_ids['b'],
        '_victims': [
            {'_victim_id': subject_ids['c'], '_explicit': True},
            {'_victim_id': subject_ids['d'], '_explicit': False}
        ]
    },
    subject_ids['c']: {
        '_id': subject_ids['c'],
        '_victims': [
            {'_victim_id': subject_ids['d'], '_explicit': True}
        ]
    },
    subject_ids['d']: {'_id': subject_ids['d']},
    subject_ids['e']: {'_id': subject_ids['e']},
}


def mock_get_subject(obj_id):
    return subject_dict[obj_id]


@patch('db.subject_storage.SubjectDAO')
@patch('flask_pymongo.PyMongo')
def test_save_choice_new_subject(mock_subject_dao, mock_pymongo):
    mock_subject_dao.get_team_record = mock_get_subject
    subject_repository = TeamRepository(None)
    subject_repository.team_dao = mock_subject_dao

    expected_subject = SubjectRecord.factory({
        '_id': subject_ids['e'],
        '_victims': [{
            '_victim_id': subject_ids['a'],
            '_explicit': True
        }, {
            '_victim_id': subject_ids['b'],
            '_explicit': False
        }, {
            '_victim_id': subject_ids['c'],
            '_explicit': False
        }, {
            '_victim_id': subject_ids['d'],
            '_explicit': False
        }]
    })

    subject_repository.save_choice([
        SubjectDTO(subject_ids['e'], selected=True),
        SubjectDTO(subject_ids['a'], selected=False)
    ])

    actual_subject = mock_subject_dao.update_victims.call_args[0][0]  # type: SubjectRecord
    validate_is_equal(expected_subject, actual_subject)


@patch('db.subject_storage.SubjectDAO')
@patch('flask_pymongo.PyMongo')
def test_save_choice_subject_with_contradictions(mock_subject_dao, mock_pymongo):
    mock_subject_dao.get_team_record = mock_get_subject
    subject_repository = TeamRepository(None)
    subject_repository.team_dao = mock_subject_dao

    expected_subject = SubjectRecord.factory({
        '_id': subject_ids['c'],
        '_victims': [{
            '_victim_id': subject_ids['a'],
            '_explicit': True
        }, {
            '_victim_id': subject_ids['d'],
            '_explicit': True
        }]
    })

    subject_repository.save_choice([
        SubjectDTO(subject_ids['c'], selected=True),
        SubjectDTO(subject_ids['a'], selected=False)
    ])

    actual_subject = mock_subject_dao.update_victims.call_args[0][0]  # type: SubjectRecord
    validate_is_equal(expected_subject, actual_subject)


def validate_is_equal(expected_subject, actual_subject):
    assert expected_subject.id == actual_subject.id
    assert expected_subject.victims == actual_subject.victims
    expected_victims = set(expected_subject.victims)
    actual_victims = set(actual_subject.victims)
    for expected_victim in expected_victims:
        is_actual = False
        for actual_victim in actual_victims:
            if expected_victim.victim_id == actual_victim.victim_id and expected_victim.explicit == actual_victim.explicit:
                is_actual = True
                break
        if not is_actual:
            assert False, 'Victim ' + str(expected_victim) + ' was not found'


if __name__ == '__main__':
    test_save_choice_new_subject()
    test_save_choice_subject_with_contradictions()
