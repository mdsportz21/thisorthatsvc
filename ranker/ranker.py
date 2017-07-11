from collections import OrderedDict

from model.record import SubjectRecord
from repository.subject_repository import SubjectRepository


class Ranker(object):
    """
    :type subject_repository: SubjectRepository
    """

    def __init__(self, subject_repository):
        self.subject_repository = subject_repository

    def get_rankings(self):
        """
        :rtype: list of SubjectRecord
        """
        ranked_subject_id_to_record_ordered_dict = OrderedDict()
        subject_dict = self.subject_repository.get_subject_record_dict()

        # Calculate front of line - this includes unconnected subjects
        head_ids = subject_dict.get_subject_ids_with_no_prev()

        non_tail_ids = set([subject.id for subject in subject_dict.get_subjects_with_next()])
        leader_ids = head_ids.intersection(non_tail_ids)
        leader_subject_records = [subject_dict.get(subject_id) for subject_id in leader_ids]
        ranked_subject_id_to_record_ordered_dict.update(
            {subject_record.id: subject_record for subject_record in leader_subject_records})

        tail_ids = set([subject.id for subject in subject_dict.get_subjects_with_no_next()])
        orphan_ids = head_ids.intersection(tail_ids)
        orphan_subject_records = [subject_dict.get(subject_id) for subject_id in orphan_ids]
        ranked_subject_id_to_record_ordered_dict.update(
            {subject_record.id: subject_record for subject_record in orphan_subject_records})

        # Calculate rest of line
        for subject_record in leader_subject_records:
            next_record = subject_dict.get_next(subject_record)
            while next_record is not None:
                ranked_subject_id_to_record_ordered_dict[next_record.id: next_record]
                next_record = subject_dict.get_next(subject_record)

        assert len(ranked_subject_id_to_record_ordered_dict) == len(subject_dict.get_subject_records())
        return ranked_subject_id_to_record_ordered_dict.values()
