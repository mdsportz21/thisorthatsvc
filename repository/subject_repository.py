from flask_pymongo import PyMongo

from db.subject_storage import SubjectDAO
from model import codec
from model.dto import SubjectDTO
from model.record import SubjectRecord
from model.record import SubjectRecordDict
from model.record import Victim


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
        :type subject_dtos: list of SubjectDTO
        """
        winner_ids = [subject_dto.subjectId for subject_dto in subject_dtos if subject_dto.selected]
        loser_ids = [subject_dto.subjectId for subject_dto in subject_dtos if not subject_dto.selected]
        for winner_id in winner_ids:
            winner_victims = self.get_or_create_victims(winner_id)
            for loser_id in loser_ids:
                winner_victims.add(Victim.create_victim(loser_id))
            self.subject_dao.udpate_victims(winner_id, winner_victims)
        for loser_id in loser_ids:
            loser_victims = self.get_or_create_victims(loser_id)
            for winner_id in winner_ids:
                loser_victims.remove(Victim.create_victim(winner_id))
            self.subject_dao.udpate_victims(loser_id, loser_victims)

    def get_or_create_victims(self, subject_id):
        """
        :param subject_id: ObjectId
        :return: set of SubjectRecord
        """
        subject_record_dict = self.get_subject_record_dict()
        subject_record = subject_record_dict.get_record(subject_id)
        victims = subject_record.victims if not None else set()
        return victims
