from flask_pymongo import PyMongo

from db.subject_storage import SubjectDAO
from model import codec
from model.dto import SubjectDTO
from model.record import SubjectRecord
from model.record import SubjectRecordDict
from bson import ObjectId


class SubjectRepository(object):
    """
    :type subject_dao: SubjectDAO
    """

    def __init__(self, app):
        self.subject_dao = SubjectDAO(PyMongo(app))

    def get_subject_records(self):
        """
        :rtype: list of SubjectDTO
        """
        return [SubjectRecord.subject_record_factory(subject_dict) for subject_dict in self.subject_dao.get_subjects()]

    def get_subject_record_dict(self):
        """
        :return: SubjectRecordDict
        """
        return SubjectRecordDict(self.get_subject_records())

    def store_subject_dtos(self, subject_dtos):
        """
        :type subject_dtos: list of SubjectDTO
        """
        subject_records = codec.to_subject_records(subject_dtos)
        self.subject_dao.store_subjects(subject_records)

    def save_choice(self, subject_dtos):
        """
        :param subject_dtos: list of SubjectDTO
        """
        winners = []
        """:type : list of SubjectDTO"""
        losers = []
        """:type : list of SubjectDTO"""
        for subject in subject_dtos:
            winners.append(subject) if subject.selected else losers.append(subject)
        for winner in winners:
            for loser in losers:
                winner_id = ObjectId(winner.subjectId)
                loser_id = ObjectId(loser.subjectId)
                subject_records_dict = SubjectRecordDict(self.get_subject_records())
                if subject_records_dict.is_greater(loser_id, winner_id):
                    winner_record = subject_records_dict.get(winner_id)
                    # winner.prev.next = winner.next
                    winner_prevs = subject_records_dict.get_prev_subjects(winner_id)
                    for winner_prev in winner_prevs:
                        if winner_record.next_subject_id is None:
                            self.subject_dao.clear_next(winner_prev.id)
                        else:
                            self.subject_dao.update_next(winner_prev.id, winner_record.next_subject_id)
                    # loser.prev.next = winner
                    loser_prevs = subject_records_dict.get_prev_subjects(loser_id)
                    for loser_prev in loser_prevs:
                        self.subject_dao.update_next(loser_prev.id, winner_id)
                    # winner.next = loser
                    self.subject_dao.update_next(winner_id, loser_id)

                # This should never happen, but we can turn this on as a sanity check
                # subject_records_dict = SubjectRecordDict(self.get_subject_records())
                # if self.is_cycle(winner, subject_records_dict):
                #     self.break_cycle(winner, subject_records_dict)

    def break_cycle(self, destination_record, subject_records_dict):
        """
        :type destination_record: SubjectRecord
        :type subject_records_dict: SubjectRecordDict
        :return: bool
        """
        source_records = subject_records_dict.get_prev_subjects(destination_record.id)
        for source_record in source_records:
            self.subject_dao.clear_next(source_record.id)

    # https://en.wikipedia.org/wiki/Cycle_detection#Tortoise_and_hare
    def is_cycle(self, starting_record, subject_records_dict):
        """
        :type starting_record: SubjectRecord
        :type subject_records_dict: SubjectRecordDict
        :return: bool
        """
        if starting_record.next_subject_id is None:
            return False
        tortoise = subject_records_dict.get_next(starting_record)
        hare = subject_records_dict.get_next(tortoise)
        while hare is not None:
            if tortoise.id == hare.id:
                return True
            tortoise = subject_records_dict.get_next(tortoise)
            hare = subject_records_dict.get_next(hare)
            hare = subject_records_dict.get_next(hare)
        return False
