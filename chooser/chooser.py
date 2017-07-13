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

    def choose_new(self, num_subjects=2):
        """
        We are only supporting choosing 2 subjects at present.
        :type num_subjects: int
        :rtype: list of SubjectRecord
        """
        """
        Prerequisites:
        Store (half) matrix of choices between two subjects
        
        def Algorithm (list of subject ids) = (list of subject ids)
            Count victories of each subject (relative to rest of group)
            Group subjects by number of victories in order (rough ordering, i.e. [BEF] [AD] [C]
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
        """
        pass



    def choose(self, num_subjects=2):
        """
        We are only supporting choosing 2 subjects at present.
        :type num_subjects: int
        :rtype: list of SubjectRecord
        """
        subject_record_dict = self.subject_repository.get_subject_record_dict()
        subjects_with_next = subject_record_dict.get_subjects_with_next()
        subjects_with_no_next = subject_record_dict.get_subjects_with_no_next()
        if len(subjects_with_next) > 0:
            if len(subjects_with_no_next) > 0:
                if len(subjects_with_next) > len(subjects_with_no_next):
                    first_choice = subjects_with_next[randint(0, len(subjects_with_next) - 1)]
                    if len(subjects_with_no_next) > 1:  # remove first_choice's next
                        subjects_with_no_next = [subject for subject in subjects_with_no_next if
                                                 first_choice.next_subject_id != subject.id]
                        second_choice = subjects_with_no_next[randint(0, len(subjects_with_no_next) - 1)]
                    return [first_choice,
                            second_choice]
                else:
                    first_choice = subjects_with_no_next[randint(0, len(subjects_with_no_next) - 1)]
                    if len(subjects_with_next) > 1:
                        subjects_with_next = [subject for subject in subjects_with_next if
                                              subject.next_subject_id != first_choice.id]
                    second_choice = subjects_with_next[randint(0, len(subjects_with_next) - 1)]
                    return [first_choice, second_choice]
            else:
                subjects_with_same_next = subject_record_dict.get_subjects_with_same_next()
                if subjects_with_same_next is not None:
                    return self.choose_any_two(subjects_with_same_next)
                else:  # pick two from next with duplicate next, otherwise, pick any two and alert UI that we're done
                    return self.choose_any_two(subjects_with_next)
        else:
            return self.choose_any_two(subjects_with_no_next)

    def choose_any_two(self, subject_records):
        """
        :type subject_records: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        indices = sample(range(0, len(subject_records)), 2)
        two_subjects = [subject_records[indices[0]], subject_records[indices[1]]]
        return two_subjects
