from bson import ObjectId

from db.storage import TeamDAO, BracketDAO, SlotDAO
from model import codec
from model.dto import TeamDTO
from model.record import TeamRecord, BracketRecord, SlotRecord


class BracketRepository(object):
    def __init__(self, pymongo):
        self.bracket_dao = BracketDAO(pymongo)

    def store_bracket(self, bracket_record):
        # type -> (BracketRecord) -> (BracketRecord)
        return self.bracket_dao.store_bracket(bracket_record)

    def get_bracket(self, name):
        bracket_dict = self.bracket_dao.get_bracket(name)
        return BracketRecord.factory(bracket_dict)

    def has_bracket(self, name):
        return self.bracket_dao.get_bracket(name) is not None


class SlotRepository(object):
    """
    :type slot_dao: SlotDAO
    """

    def __init__(self, pymongo):
        self.slot_dao = SlotDAO(pymongo)

    def get_slots(self, bracket_id):
        # type: (ObjectId) -> list[SlotRecord]
        return [SlotRecord.factory(slot_dict) for slot_dict in self.slot_dao.get_slots(bracket_id)]


class TeamRepository(object):
    """
    :type team_dao: TeamDAO
    """

    def __init__(self, pymongo):
        self.team_dao = TeamDAO(pymongo)

    def get_team_records(self):
        # type: () -> list[TeamRecord]
        return [TeamRecord.factory(team_dict) for team_dict in self.team_dao.get_team_records()]

    def get_team_record(self, team_id):
        # type: () -> TeamRecord
        team_record_dict = self.team_dao.get_team_record(team_id)
        return TeamRecord.factory(team_record_dict)

    def store_team_dtos(self, team_dtos):
        # type: (list[TeamDTO]) -> None
        subject_records = codec.to_subject_records(team_dtos)
        self.team_dao.store_team_records(subject_records)
