from bson import ObjectId

from model.record import SubjectRecord
from model.record import Victim
from repository.subject_repository import SubjectRepository


class SubjectRecordDict(object):
    """
    :type subject_records: list of SubjectRecord
    :type subject_records_dict: dict[ObjectId, SubjectRecord]
    """

    def __init__(self, subject_repository):
        """
        :type subject_repository: SubjectRepository
        """
        self.subject_records = subject_repository.get_subject_records()
        self.subject_records_dict = {record.id: record for record in self.subject_records}

    def get_record(self, subject_id):
        """
        :type subject_id: ObjectId
        :rtype: SubjectRecord
        """
        return self.subject_records_dict[subject_id]

    def get_subject_records(self):
        """
        :rtype: list of SubjectRecord
        """
        return self.subject_records

    def was_compared(self, subject_one_id, subject_two_id):
        """
        :type subject_one_id: ObjectId
        :type subject_two_id: ObjectId
        :rtype: bool
        """
        subject_one = self.get_record(subject_one_id)
        subject_two = self.get_record(subject_two_id)
        return Victim.create_victim(subject_one_id) in subject_two.victims or Victim.create_victim(
            subject_two_id) in subject_one.victims

    def get_not_victim_ids(self, subject_one_id):
        """
        :type subject_one_id: ObjectId
        :rtype: set of ObjectId
        """
        subject_one = self.get_record(subject_one_id)
        victim_ids = set([victim.victim_id for victim in subject_one.victims])
        subject_ids = set([subject_record.id for subject_record in self.get_subject_records()])
        return subject_ids.difference(victim_ids).difference({subject_one_id})

    def get_not_compared_ids(self, subject_record_id):
        """
        :type subject_record_id: ObjectId
        :return: list of ObjectId
        """
        subject_ids = set([subject_record.id for subject_record in self.get_subject_records()])
        subject_ids.remove(subject_record_id)
        not_compared_ids = [other_id for other_id in subject_ids if
                            not self.was_compared(subject_record_id, other_id)]
        return not_compared_ids

    def get_loss_ids(self, subject_record_id):
        """
        :type subject_record_id: ObjectId
        :rtype: set of ObjectId
        """
        subject_ids = set([subject_record.id for subject_record in self.get_subject_records()])
        subject_ids.remove(subject_record_id)
        subject_record = self.get_record(subject_record_id)
        victim_ids = [victim.victim_id for victim in subject_record.victims]
        victorious_opponent_ids = [other_id for other_id in subject_ids if
                                   (self.was_compared(subject_record_id, other_id) and other_id not in victim_ids)]
        return victorious_opponent_ids

    def get_compared_count(self, subject_record_id):
        """
        :type subject_record_id: ObjectId
        :rtype: int
        """
        subject_record = self.get_record(subject_record_id)
        return len(subject_record.victims) + len(self.get_loss_ids(subject_record_id))

    def get_subject_record_ids_by_compared_count(self):
        """
        :rtype: dict[int, list of ObjectId]
        """
        result = {}
        for subject_record in self.get_subject_records():
            subject_record_id = subject_record.id
            compared_count = self.get_compared_count(subject_record_id)
            result.setdefault(compared_count, []).append(subject_record_id)
        return result

    def is_all_compared(self):
        """
        :rtype: bool
        """
        subject_record_ids_by_compared_count = self.get_subject_record_ids_by_compared_count()
        if len(subject_record_ids_by_compared_count) == 0:
            return True
        if len(subject_record_ids_by_compared_count) > 1:
            return False
        count = next(iter(subject_record_ids_by_compared_count))
        if count == len(self.get_subject_records()) - 1:
            return True
        return False
