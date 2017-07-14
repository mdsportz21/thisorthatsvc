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
        subject_records = self.subject_repository.get_subject_records()
        result = self.rank_subject_records(subject_records)

    def rank_subject_records(self, subject_records):
        """
        Prerequisites:
        Store (half) matrix of choices between two subjects

        def Algorithm (list of subject ids) = (list of subject ids)
            Count victories of each subject (relative to rest of group)
            Group subjects by number of victories in order (rough ordering, i.e. {3:[B,E,F], 2:[A,D], 1:[C]}
            result = []
            if multiple groups:
                For each group:
                    result.extend(Algorithm(group)) # Combine the sorted groups in order
            elif single element group:
                result = group
            else:
                # manual sort
                result = group
                decisions_sorted_by_date_asc = get()
                for each decision:
                    result = reorder_by_moving_ahead(result, winner, loser)
            return result


        Notes:
        * maybe use default_dict for matrix? http://thinknook.com/two-dimensional-python-matrix-data-structure-with-string-indices-2013-01-17/
        * use Counter::most_common() for ordering algorithm: https://docs.python.org/2/library/collections.html#counter-objects
        ** Loop through these to create count groups, and sort the groups recursively

        We are only supporting choosing 2 subjects at present.
        Returns subject records in order of ranking
        :type subject_records: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        result = []
        # count relative to other subjects in list
        subject_records_by_victim_count = Ranker.get_subject_records_by_victim_count(subject_records)  # Bucket
        if len(subject_records_by_victim_count) == 0:
            return []
        if len(subject_records_by_victim_count) > 1:
            for subject_record_tuple in sorted(subject_records_by_victim_count.items(),
                                               key=lambda subjects_tuple: subjects_tuple[0], reverse=True):  # Sort buckets
                subject_record_group = subject_record_tuple[1]
                result.extend(self.rank_subject_records(subject_record_group))
        else:
            subject_record_group = subject_records_by_victim_count.itervalues().next()  # only group
            result = subject_record_group
            if len(subject_record_group) > 1:
                # manual sort
                # get all comparisons in this format (my_subject_id, victim_subject_id, date)
                comparison_subject_records = []
                for subject_record in subject_record_group:
                    # Bastardizing the SubjectRecord class for comparisons
                    comparison_subject_records.extend(
                        list(map((lambda victim: SubjectRecord(_id=subject_record.id, victims=[victim])),
                                 subject_record.victims)))
                comparison_subject_records_by_date_asc = sorted(comparison_subject_records,
                                                                key=lambda record: record.victims[
                                                                    0].battle_date)  # type: list [SubjectRecord]
                for comparison_subject_record in comparison_subject_records_by_date_asc:
                    winner_index = result.index(SubjectRecord(_id=comparison_subject_record.id))
                    loser_index = result.index(SubjectRecord(_id=comparison_subject_record.victims[0].victim_id))
                    if winner_index > loser_index:
                        result.insert(loser_index, result.pop(winner_index))

        return result

    @staticmethod
    def get_subject_records_by_victim_count(subject_records):
        """
        For each subject_record, get number of victories relative to the rest of the list.
        Return list of subject records by number of victims.

        :type subject_records: list of SubjectRecord
        :rtype: dict[int, list of SubjectRecord]
        """
        result = {}
        subject_record_ids = [subject_record.id for subject_record in subject_records]
        for subject_record in subject_records:
            victim_ids = [victim.victim_id for victim in subject_record.victims]
            num_victories = sum(1 if victim_id in subject_record_ids else 0 for victim_id in victim_ids)
            result.setdefault(num_victories, []).append(subject_record)
        return result
