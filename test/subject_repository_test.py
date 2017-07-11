from bson.objectid import ObjectId
from mock import patch

from db.subject_storage import SubjectDAO
from model.record import SubjectRecord
from model.record import SubjectRecordDict
from repository.subject_repository import SubjectRepository

# def fake_init(self, app):
#     self.subject_dao = SubjectDAO(None)


starting_record = SubjectRecord(_id=ObjectId("595f20b3d6f45f8761e47f9c"),
                                img_desc="Charleston River Dogs",
                                description="C-Town River Dogs",
                                img_link="https://static1.squarespace.com/static/594061048419c282ed731d4a/5949b25b86e6c05c7d5cf26d/5949b27f6b8f5bfb66cee7e1/1498002048239/thumb+%2814%29.jpeg?format=1500w",
                                next_subject_id=ObjectId("595f20b3d6f45f8761e47f9d"))


def fake_get_subjects(self):
    return [
        starting_record,
        SubjectRecord(_id=ObjectId("595f20b3d6f45f8761e47f9d"),
                      img_desc="Augusta Greenjackets",
                      description="Augusta Greenjackets",
                      img_link="https://static1.squarespace.com/static/594061048419c282ed731d4a/59420b38893fc0f697291aa6/59420c2cb3db2bab436210dc/1497500717718/thumb.jpeg?format=1500w",
                      next_subject_id=ObjectId("595f20b3d6f45f8761e47f9e")),
        SubjectRecord(_id=ObjectId("595f20b3d6f45f8761e47f9e"),
                      img_desc="Biloxi Shuckers",
                      description="Biloxi Shuckers",
                      img_link="https://static1.squarespace.com/static/594061048419c282ed731d4a/5942ff9f3e00be915c807ade/59443fdb17bffcdd0ef9e6fe/1497645020298/thumb+%282%29.jpeg?format=2500w",
                      next_subject_id=ObjectId("595f20b3d6f45f8761e47f9f")),
        SubjectRecord(_id=ObjectId("595f20b3d6f45f8761e47f9f"),
                      img_desc="Burlington Bees",
                      description="Burlington Bees",
                      img_link="https://static1.squarespace.com/static/594061048419c282ed731d4a/59496f1fdb29d6f4e5731f2d/59496f3d414fb5804d2dab58/1497984834262/thumb+%2810%29.jpeg?format=2500w",
                      next_subject_id=ObjectId("595f20b3d6f45f8761e47f9c"))
    ]


subject_records_dict = SubjectRecordDict(fake_get_subjects(None))


# @patch.object(SubjectRepository, '__init__', fake_init)
# @patch.object(SubjectDAO, 'get_subjects', fake_get_subjects)
def test_is_cycle():
    print 'starting test_is_cycle...'
    repo = SubjectRepository(None)
    is_cycle = repo.is_cycle(starting_record, subject_records_dict)
    print 'is_cycle = ', is_cycle
    assert is_cycle is True


def fake_clear_next(self, source_record_id):
    print "Clearing next_subject_id for", source_record_id
    subject_records_dict.get(source_record_id).next_subject_id = None


@patch.object(SubjectDAO, 'clear_next', fake_clear_next)
def test_break_cycle():
    print 'starting test_is_cycle...'
    repo = SubjectRepository(None)
    prev_subject = subject_records_dict.get_prev_subjects(starting_record.id)[0]
    repo.break_cycle(starting_record, subject_records_dict)
    assert prev_subject.next_subject_id is None

if __name__ == '__main__':
    test_is_cycle()
