from bson import ObjectId
from flask_pymongo import PyMongo

from db.subject_storage import SubjectDAO
from model import codec
from model.dto import SubjectDTO
from model.record import SubjectRecord
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

    def get_subject_record(self, subject_id):
        """
        :type subject_id: ObjectId
        :rtype: SubjectRecord
        """
        subject_record_dict = self.subject_dao.get_subject(subject_id)
        subject_record = SubjectRecord.subject_record_factory(subject_record_dict)
        return subject_record

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
            winner_subject = self.get_record(winner_id)
            winner_victims = winner_subject.victims
            for loser_id in loser_ids:
                winner_victims.add(Victim.create_victim(loser_id))
            self.subject_dao.update_victims(winner_id, winner_victims)
        for loser_id in loser_ids:
            loser_subject = self.get_record(loser_id)
            loser_victims = loser_subject.victims
            for winner_id in winner_ids:
                loser_victims.remove(Victim.create_victim(winner_id))
            self.subject_dao.update_victims(loser_id, loser_victims)
