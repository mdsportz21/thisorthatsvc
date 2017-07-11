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

    def choose_any_two(self, subjects):
        """
        :type subjects: list of SubjectRecord
        :rtype: list of SubjectRecord
        """
        two_subjects = []
        indices = sample(range(0, len(subjects)), 2)
        two_subjects.append(subjects[indices[0]])
        two_subjects.append(subjects[indices[1]])
        return two_subjects
