from bson import ObjectId

from model.record import SubjectRecord
from model.record import Victim
from ranker.ranker import Ranker

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
                  victims=[Victim.create_victim(subject_ids['c']), Victim.create_victim(subject_ids['e'])]),
    SubjectRecord(_id=subject_ids['b'],
                  victims=[Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['d']),
                           Victim.create_victim(subject_ids['f'])]),
    SubjectRecord(_id=subject_ids['c'],
                  victims=[Victim.create_victim(subject_ids['b']), Victim.create_victim(subject_ids['e'])]),
    SubjectRecord(_id=subject_ids['d'],
                  victims=[Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['c']),
                           Victim.create_victim(subject_ids['f'])]),
    SubjectRecord(_id=subject_ids['e'],
                  victims=[Victim.create_victim(subject_ids['b']), Victim.create_victim(subject_ids['d'])]),
    SubjectRecord(_id=subject_ids['f'],
                  victims=[Victim.create_victim(subject_ids['a']), Victim.create_victim(subject_ids['c']),
                           Victim.create_victim(subject_ids['e'])])
]


def test_rank_subject_records():
    ranker = Ranker(None)
    ranked_records = ranker.rank_subject_records(test_rank_subject_records_data)
    assert len(ranked_records) == 6
    assert ranked_records[0].id == subject_ids['b']


if __name__ == '__main__':
    test_rank_subject_records()
