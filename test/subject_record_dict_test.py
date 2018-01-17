from bson import ObjectId
from mock import patch

from model.record import SubjectRecord
from model.record import Victim
from subject_record_dict import SubjectRecordDict

subject_ids = {
    'a': ObjectId(24 * 'a'),
    'b': ObjectId(24 * 'b'),
    'c': ObjectId(24 * 'c'),
    'd': ObjectId(24 * 'd'),
    'e': ObjectId(24 * 'e'),
    'f': ObjectId(24 * 'f')
}


def create_subject_record_dict(mock_subject_repository, get_subject_records_return_value):
    mock_subject_repository.get_team_records.return_value = get_subject_records_return_value
    subject_record_dict = SubjectRecordDict(mock_subject_repository)
    return subject_record_dict


@patch('repository.subject_repository.SubjectRepository')
def test_is_all_compared_all_compared(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b'])
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    is_all_compared = subject_record_dict.are_all_subjects_compared()

    assert is_all_compared


@patch('repository.subject_repository.SubjectRepository')
def test_is_all_compared_all_not_compared(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'])
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    is_all_compared = subject_record_dict.are_all_subjects_compared()

    assert not is_all_compared


@patch('repository.subject_repository.SubjectRepository')
def test_get_subject_record_ids_by_compared_count(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'])
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    subject_record_ids_by_compared_count = subject_record_dict.get_subject_record_ids_by_compared_count()
    assert len(subject_record_ids_by_compared_count) == 2
    assert 1 in subject_record_ids_by_compared_count
    subjects_with_one_compared = subject_record_ids_by_compared_count[1]
    assert len(subjects_with_one_compared) == 2
    assert subject_ids['a'] in subjects_with_one_compared
    assert subject_ids['b'] in subjects_with_one_compared

    assert 0 in subject_record_ids_by_compared_count
    subjects_with_zero_compared = subject_record_ids_by_compared_count[0]
    assert len(subjects_with_zero_compared) == 1
    assert subject_ids['c'] in subjects_with_zero_compared


@patch('repository.subject_repository.SubjectRepository')
def test_get_compared_count(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'])
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    a_count = subject_record_dict.get_compared_count(subject_ids['a'])
    assert a_count == 1

    b_count = subject_record_dict.get_compared_count(subject_ids['b'])
    assert b_count == 1

    c_count = subject_record_dict.get_compared_count(subject_ids['c'])
    assert c_count == 0


@patch('repository.subject_repository.SubjectRepository')
def test_get_loss_ids(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'], victims={Victim.create_victim(subject_ids['b'])})
    ]

    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    b_loss_ids = subject_record_dict.get_loss_ids(subject_ids['b'])
    assert len(b_loss_ids) == 2
    assert subject_ids['a'] in b_loss_ids
    assert subject_ids['c'] in b_loss_ids

    a_loss_ids = subject_record_dict.get_loss_ids(subject_ids['a'])
    assert len(a_loss_ids) == 0


@patch('repository.subject_repository.SubjectRepository')
def test_get_not_compared_ids(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'], victims={Victim.create_victim(subject_ids['b'])})
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    a_not_compared_ids = subject_record_dict.get_not_compared_ids(subject_ids['a'])
    assert len(a_not_compared_ids) == 1
    assert a_not_compared_ids[0] == subject_ids['c']


@patch('repository.subject_repository.SubjectRepository')
def test_get_not_victim_ids(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'], victims={Victim.create_victim(subject_ids['b'])})
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    a_not_victim_ids = subject_record_dict.get_not_victim_ids(subject_ids['a'])
    assert len(a_not_victim_ids) == 1
    assert next(iter(a_not_victim_ids)) == subject_ids['c']

    b_not_victim_ids = subject_record_dict.get_not_victim_ids(subject_ids['b'])
    assert len(b_not_victim_ids) == 2
    assert subject_ids['a'] in b_not_victim_ids
    assert subject_ids['c'] in b_not_victim_ids


@patch('repository.subject_repository.SubjectRepository')
def test_was_compared(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'], victims={Victim.create_victim(subject_ids['b'])})
    ]
    subject_record_dict = create_subject_record_dict(mock_subject_repository, test_data)

    ab_was_compared = subject_record_dict.was_compared(subject_ids['a'], subject_ids['b'])
    assert ab_was_compared
    bc_was_compared = subject_record_dict.was_compared(subject_ids['b'], subject_ids['c'])
    assert bc_was_compared
    ac_was_compared = subject_record_dict.was_compared(subject_ids['a'], subject_ids['c'])
    assert not ac_was_compared


if __name__ == '__main__':
    test_get_subject_record_ids_by_compared_count()
