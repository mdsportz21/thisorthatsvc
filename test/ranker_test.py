from bson import ObjectId
from mock import patch

from model.record import SubjectRecord
from model.record import Victim
from ranker import Ranker
from subject_record_dict import SubjectRecordDict

subject_ids = {
    'a': ObjectId(24 * 'a'),
    'b': ObjectId(24 * 'b'),
    'c': ObjectId(24 * 'c'),
    'd': ObjectId(24 * 'd'),
    'e': ObjectId(24 * 'e'),
    'f': ObjectId(24 * 'f')
}

test_rank_subject_records_data = [
    SubjectRecord(_id=subject_ids['a'],
                  victims={Victim.create_victim(subject_ids['c']), Victim.create_victim(subject_ids['e'])}),
    SubjectRecord(_id=subject_ids['b'],
                  victims={Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['d']),
                           Victim.create_victim(subject_ids['f'])}),
    SubjectRecord(_id=subject_ids['c'],
                  victims={Victim.create_victim(subject_ids['b']), Victim.create_victim(subject_ids['e'])}),
    SubjectRecord(_id=subject_ids['d'],
                  victims={Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['c']),
                           Victim.create_victim(subject_ids['f'])}),
    SubjectRecord(_id=subject_ids['e'],
                  victims={Victim.create_victim(subject_ids['b']), Victim.create_victim(subject_ids['d'])}),
    SubjectRecord(_id=subject_ids['f'],
                  victims={Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['c']),
                           Victim.create_victim(subject_ids['e'])})
]

test_rank_subject_records_no_victims_data = [
    SubjectRecord(_id=subject_ids['a']),
    SubjectRecord(_id=subject_ids['b']),
    SubjectRecord(_id=subject_ids['c']),
    SubjectRecord(_id=subject_ids['d']),
    SubjectRecord(_id=subject_ids['e']),
    SubjectRecord(_id=subject_ids['f'])
]


@patch('repository.subject_repository.SubjectRepository')
def test_get_rankings(mock_subject_repository):
    mock_subject_repository.get_team_records.return_value = test_rank_subject_records_data
    subject_record_dict = SubjectRecordDict(mock_subject_repository)
    ranker = Ranker(subject_record_dict)
    ranked_records = ranker.get_rankings()
    assert len(ranked_records) == 6
    assert ranked_records[0].id == subject_ids['b']
    assert ranked_records[1].id == subject_ids['d']
    assert ranked_records[2].id == subject_ids['f']
    assert ranked_records[3].id == subject_ids['a']
    assert ranked_records[4].id == subject_ids['c']
    assert ranked_records[5].id == subject_ids['e']


@patch('repository.subject_repository.SubjectRepository')
def test_get_rankings_no_victims(mock_subject_repository):
    mock_subject_repository.get_team_records.return_value = test_rank_subject_records_no_victims_data
    subject_record_dict = SubjectRecordDict(mock_subject_repository)
    ranker = Ranker(subject_record_dict)
    ranked_records = ranker.get_rankings()
    assert len(ranked_records) == 6


if __name__ == '__main__':
    test_get_rankings()
