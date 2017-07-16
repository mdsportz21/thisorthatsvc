import util
from model.record import SubjectRecord
from subject_record_dict import SubjectRecordDict


class Ranker(object):
    """
    :type subject_record_dict: SubjectRecordDict
    """

    def __init__(self, subject_record_dict):
        self.subject_record_dict = subject_record_dict

    def get_rankings(self):
        """
        :rtype: list of SubjectRecord
        """
        subject_records = self.subject_record_dict.get_subject_records()
        result = self.rank_subject_records(subject_records)
        return result

    def rank_subject_records(self, subject_records):
        """
        Uses recursive bucket sort to sort subjects by relative number of victims.
        Tie breaker is most recent date of comparison.
        Returns subject records in order of ranking.

        We are only supporting choosing 2 subjects at present.

        :type subject_records: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        result = []
        # count relative to other subjects in list
        subject_records_by_victim_count = self.get_subject_records_by_winning_percentage(subject_records)  # Bucket
        if len(subject_records_by_victim_count) == 0:
            return []
        if len(subject_records_by_victim_count) > 1:
            subjects_by_victim_count_desc = sorted(subject_records_by_victim_count.items(),
                                                   key=lambda subjects_tuple: subjects_tuple[0],
                                                   reverse=True)
            for subject_record_tuple in subjects_by_victim_count_desc:  # Sort buckets
                subject_record_group = subject_record_tuple[1]
                result.extend(self.rank_subject_records(subject_record_group))
        else:
            subject_record_group = subject_records_by_victim_count.itervalues().next()  # only group
            result = subject_record_group
            if len(subject_record_group) > 1:  # more than one subject in group
                # manual sort
                comparison_subject_records = []  # get all comparisons as (my_subject_id, victim_subject_id, date)
                for subject_record in subject_record_group:
                    # Bastardizing the SubjectRecord class for comparisons
                    comparison_subject_records.extend(
                        list(map((lambda victim: SubjectRecord(_id=subject_record.id, victims={victim})),
                                 subject_record.victims)))
                comparison_subject_records_by_date_asc = sorted(comparison_subject_records,
                                                                key=lambda record: next(iter(record.victims)).battle_date)  # type: list [SubjectRecord]
                for comparison_subject_record in comparison_subject_records_by_date_asc:
                    winner_index = result.index(SubjectRecord(_id=comparison_subject_record.id))
                    loser_index = result.index(SubjectRecord(_id=next(iter(comparison_subject_record.victims)).victim_id))
                    if winner_index > loser_index:
                        result.insert(loser_index, result.pop(winner_index))

        return result

    @staticmethod
    def get_subject_records_by_victim_count(subject_records):
        """
        For each subject_record, get number of victories RELATIVE TO THE REST OF THE LIST.
        Return list of subject records by number of victims.

        :type subject_records: list of SubjectRecord
        :rtype: dict[int, list of SubjectRecord]
        """
        result = {}
        subject_record_ids = [subject_record.id for subject_record in subject_records]
        for subject_record in subject_records:
            victim_ids = [victim.victim_id for victim in subject_record.victims]
            num_relative_victories = sum(1 if victim_id in subject_record_ids else 0 for victim_id in victim_ids)
            result.setdefault(num_relative_victories, []).append(subject_record)
        return result

    def get_subject_records_by_winning_percentage(self, subject_records):
        result = {}
        subject_record_ids = [subject_record.id for subject_record in subject_records]
        for subject_record in subject_records:
            victim_ids = [victim.victim_id for victim in subject_record.victims]
            local_win_count = sum(
                1 if subject_record_id in subject_record_ids else 0 for subject_record_id in victim_ids)
            loss_ids = self.subject_record_dict.get_loss_ids(subject_record.id)
            faced_ids = victim_ids + list(loss_ids)
            local_faced_count = sum(
                1 if subject_record_id in subject_record_ids else 0 for subject_record_id in faced_ids)
            local_winning_percentage = util.divide(local_win_count, local_faced_count) if local_faced_count != 0 else 0
            result.setdefault(local_winning_percentage, []).append(subject_record)
        return result
