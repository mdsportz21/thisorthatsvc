from bson import ObjectId
from mock import patch

from chooser.chooser import Chooser
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


def create_chooser(mock_subject_repository, get_subject_records_return_value):
    mock_subject_repository.get_team_records.return_value = get_subject_records_return_value
    subject_record_dict = SubjectRecordDict(mock_subject_repository)
    chooser = Chooser(subject_record_dict)
    return chooser


@patch('repository.subject_repository.SubjectRepository')
def test_choose(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'], victims={Victim.create_victim(subject_ids['b'])}),
        SubjectRecord(_id=subject_ids['b']),
        SubjectRecord(_id=subject_ids['c'], victims={Victim.create_victim(subject_ids['b'])})
    ]
    chooser = create_chooser(mock_subject_repository, test_data)
    subject_records = chooser.choose()
    assert len(subject_records) == 2
    subject_record_ids = [subject_record.id for subject_record in subject_records]
    assert subject_ids['a'] in subject_record_ids
    assert subject_ids['c'] in subject_record_ids


@patch('repository.subject_repository.SubjectRepository')
def test_choose_2(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'],  # 4-0
                      victims={
                          Victim.create_victim(subject_ids['b']),
                          Victim.create_victim(subject_ids['c']),
                          Victim.create_victim(subject_ids['d'])}),
        SubjectRecord(_id=subject_ids['b'],  # 2-1
                      victims={
                          Victim.create_victim(subject_ids['c']),
                          Victim.create_victim(subject_ids['e'])}),
        SubjectRecord(_id=subject_ids['c']),  # 0-2
        SubjectRecord(_id=subject_ids['d']),  # 0-1
        SubjectRecord(_id=subject_ids['e'])  # 0-1
    ]

    chooser = create_chooser(mock_subject_repository, test_data)
    subject_records = chooser.choose()
    assert len(subject_records) == 2
    subject_record_ids = [subject_record.id for subject_record in subject_records]
    assert subject_ids['d'] in subject_record_ids
    assert subject_ids['e'] in subject_record_ids


@patch('repository.subject_repository.SubjectRepository')
def test_get_percentage_completed(mock_subject_repository):
    test_data = [
        SubjectRecord(_id=subject_ids['a'],  # 4-0
                      victims={
                          Victim.create_victim(subject_ids['b']),
                          Victim.create_victim(subject_ids['c']),
                          Victim.create_victim(subject_ids['d']),
                          Victim.create_victim(subject_ids['e'])}),
        SubjectRecord(_id=subject_ids['b'],  # 2-1
                      victims={
                          Victim.create_victim(subject_ids['c']),
                          Victim.create_victim(subject_ids['d']),
                          Victim.create_victim(subject_ids['e'])}),
        SubjectRecord(_id=subject_ids['c']),  # 0-2
        SubjectRecord(_id=subject_ids['d']),  # 0-1
        SubjectRecord(_id=subject_ids['e']),  # 0-1
        SubjectRecord(_id=subject_ids['f'])  # 0-1
    ]

    chooser = create_chooser(mock_subject_repository, test_data)
    percentage_completed = chooser.get_percentage_completed()
    expected_percentaged_completed = 7 / float(15)
    assert abs(expected_percentaged_completed - percentage_completed) <= 0.001


if __name__ == '__main__':
    test_get_percentage_completed()
