from bson import ObjectId

from db.storage import SubjectDAO, BracketDAO
from model import codec
from model.dto import SubjectDTO
from model.record import SubjectRecord, Victim, Bracket


class BracketRepository(object):
    def __init__(self, pymongo):
        self.bracket_dao = BracketDAO(pymongo)

    def store_bracket(self, bracket):
        self.bracket_dao.store_bracket(bracket)

    def get_bracket(self, name):
        bracket_dict = self.bracket_dao.get_bracket(name)
        return Bracket.factory(bracket_dict)

class SubjectRepository(object):
    """
    :type subject_dao: SubjectDAO
    """

    def __init__(self, pymongo):
        self.subject_dao = SubjectDAO(pymongo)

    def get_subject_records(self):
        """
        :rtype: list of SubjectDTO
        """
        return [SubjectRecord.factory(subject_dict) for subject_dict in self.subject_dao.get_subjects()]

    def get_subject_record(self, subject_id):
        """
        :type subject_id: ObjectId
        :rtype: SubjectRecord
        """
        subject_record_dict = self.subject_dao.get_subject(subject_id)
        subject_record = SubjectRecord.factory(subject_record_dict)
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
        subjects_to_update = set()

        for winner_id in winner_ids:
            winner_subject = self.get_subject_record(winner_id)
            subjects_to_update.add(winner_subject)

            for loser_id in loser_ids:
                winner_subject.victims.add(Victim.create_victim(loser_id, True))

                loser_subject = self.get_subject_record(loser_id)
                if winner_subject.as_victim() in loser_subject.victims:
                    loser_subject.victims.remove(winner_subject.as_victim())
                    subjects_to_update.add(loser_subject)

                for losers_victim in loser_subject.victims:
                    victim_subject = self.get_subject_record(losers_victim.victim_id)
                    if winner_subject.as_victim() in victim_subject.victims:
                        winner_victim = None
                        for v in victim_subject.victims:
                            if v == winner_subject.as_victim():
                                winner_victim = v
                                break
                        if not winner_victim.explicit:
                            winner_subject.victims.add(Victim.create_victim(losers_victim.victim_id, False))
                            victim_subject.victims.remove(winner_subject.as_victim())
                            subjects_to_update.add(victim_subject)
                    else:
                        winner_subject.victims.add(Victim.create_victim(losers_victim.victim_id, False))

        for subject_to_update in subjects_to_update:
            self.subject_dao.update_victims(subject_to_update)
