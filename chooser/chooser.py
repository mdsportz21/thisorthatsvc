from random import sample

from model.record import SubjectRecord
from subject_record_dict import SubjectRecordDict


class Chooser(object):
    """
    :type subject_record_dict: SubjectRecordDict
    """

    def __init__(self, subject_record_dict):
        self.subject_record_dict = subject_record_dict

    def choose(self):
        """
        Choose the subject with the least comparisons.
        Compare it to a subject it has not yet been compared to, at random.

        Note: We are only supporting choosing 2 subjects at present.

        :rtype: list of SubjectRecord
        """
        if self.subject_record_dict.is_all_compared():
            return self.choose_any_two(self.subject_record_dict.get_subject_records())

        subject_record_ids_by_compared_count = self.subject_record_dict.get_subject_record_ids_by_compared_count()
        sorted_subject_ids_by_count = sorted(subject_record_ids_by_compared_count.items())
        subject_record_id_with_lowest_count = sorted_subject_ids_by_count[0][1][0]
        not_compared_ids = self.subject_record_dict.get_not_compared_ids(subject_record_id_with_lowest_count)
        subject_record_with_lowest_count = self.subject_record_dict.get_record(subject_record_id_with_lowest_count)

        # lowest comparison count uncompared
        for count, subject_ids in sorted_subject_ids_by_count:
            for subject_id in subject_ids:
                if subject_record_id_with_lowest_count == subject_id:
                    continue
                if subject_id in not_compared_ids:
                    uncompared_subject_record = self.subject_record_dict.get_record(subject_id)
                    return [subject_record_with_lowest_count, uncompared_subject_record]

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
