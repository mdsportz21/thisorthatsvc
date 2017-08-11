from random import sample

from model.record import SubjectRecord
from subject_record_dict import SubjectRecordDict
from ranker.ranker import Ranker


class Chooser(object):
    """
    :type subject_record_dict: SubjectRecordDict
    :type ranker: Ranker
    """

    def __init__(self, subject_record_dict, ranker):
        self.subject_record_dict = subject_record_dict
        self.ranker = ranker

    def choose(self):
        """
        Choose the subject with the most comparisons.
        Get the subjects it has not been compared to yet, in order of ranking
        Choose the middle ranked subject

        Note: We are only supporting choosing 2 subjects at present.

        :rtype: list of SubjectRecord
        """
        if self.subject_record_dict.is_all_compared():
            return self.choose_any_two(self.subject_record_dict.get_subject_records())

        subject_record_ids_by_compared_count = self.subject_record_dict.get_subject_record_ids_by_compared_count()
        counts = sorted(subject_record_ids_by_compared_count.keys(), reverse=True)
        has_all_compared = counts[0] == len(self.subject_record_dict.subject_records) - 1
        if len(counts) == 1 or not has_all_compared:
            target_count = counts[0]
        else:
            target_count = counts[1]
        subject_one_id = subject_record_ids_by_compared_count[target_count][0]
        subject_record_one = self.subject_record_dict.get_record(subject_one_id)

        not_compared_ids = self.subject_record_dict.get_not_compared_ids(subject_one_id)
        sorted_not_compared_ids = self.ranker.sort_ids_by_ranking(not_compared_ids)
        subject_two_id = sorted_not_compared_ids[len(sorted_not_compared_ids)/2]
        subject_record_two = self.subject_record_dict.get_record(subject_two_id)

        return [subject_record_one, subject_record_two]

    @staticmethod
    def choose_any_two(subject_records):
        """
        :type subject_records: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        indices = sample(range(0, len(subject_records)), 2)
        two_subjects = [subject_records[indices[0]], subject_records[indices[1]]]
        return two_subjects

    def get_percentage_completed(self):
        """
        :rtype: float
        """
        num_comparisons = 0
        subject_records = self.subject_record_dict.subject_records
        for subject_record in subject_records:
            num_comparisons += len(subject_record.victims)
        num_possible_comparisons = sum(i for i in range(1, len(subject_records)))
        return num_comparisons / float(num_possible_comparisons)
