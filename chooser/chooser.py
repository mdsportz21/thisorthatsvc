from random import randint
from random import sample

from model.record import SubjectRecord
from repository.subject_repository import SubjectRepository


class Chooser(object):
    """
    :type subject_repository: SubjectRepository
    """

    def __init__(self, subject_repository):
        self.subject_repository = subject_repository

    def choose(self, num_subjects=2):
        """
        Alg ideas:
        1. Pick any combination that doesn't exist yet
        2. Give precedence to
            1) comparisons that don't exist
            2) comparisons that don't match (least match) ranking

        Note: We are only supporting choosing 2 subjects at present.

        :type num_subjects: int
        :rtype: list of SubjectRecord
        """
        pass

    def choose_any_two(self, subject_records):
        """
        :type subject_records: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        indices = sample(range(0, len(subject_records)), 2)
        two_subjects = [subject_records[indices[0]], subject_records[indices[1]]]
        return two_subjects
