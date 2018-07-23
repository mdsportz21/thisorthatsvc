from typing import List

from bson import ObjectId

from db.storage import TeamDAO, BracketDAO
from model import codec
from model.dto import TeamDTO
from model.record import TeamRecord, BracketFieldRecord


class BracketRepository(object):
    def __init__(self, pymongo):
        self.bracket_dao = BracketDAO(pymongo)

    def create_bracket_field(self, bracket_field_name, team_records):
        # type (str, list[TeamRecord]) -> None
        bracket_field_record = BracketFieldRecord(_id=ObjectId(), name=bracket_field_name, team_records=team_records)
        self.bracket_dao.store_bracket_field(bracket_field_record)

    def get_all_bracket_field_records(self):
        # type: (BracketRepository) -> List[BracketFieldRecord]
        return [BracketFieldRecord.from_document(doc) for doc in self.bracket_dao.get_all_bracket_field_documents()]

    # def store_bracket(self, bracket_record):
    #     # type -> (BracketRecord) -> (BracketRecord)
    #     return self.bracket_dao.store_bracket(bracket_record)
    #
    # def get_bracket(self, name):
    #     bracket_dict = self.bracket_dao.get_bracket(name)
    #     return BracketRecord.factory(bracket_dict) if bracket_dict is not None else None
    #
    # def has_bracket(self, name):
    #     return self.bracket_dao.get_bracket(name) is not None


class TeamRepository(object):
    """
    :type team_dao: TeamDAO
    """

    def __init__(self, pymongo):
        self.team_dao = TeamDAO(pymongo)

    def get_team_records(self):
        # type: () -> list[TeamRecord]
        return [TeamRecord.from_document(team_dict) for team_dict in self.team_dao.get_team_documents()]

    def get_team_record(self, team_id):
        # type: () -> TeamRecord
        team_record_dict = self.team_dao.get_team_document(team_id)
        return TeamRecord.from_document(team_record_dict)

    def store_team_dtos(self, team_dtos):
        # type: (list[TeamDTO]) -> None
        subject_records = codec.to_subject_records(team_dtos)
        self.team_dao.store_team_records(subject_records)

    def get_group_with_max_count(self):
        return [TeamRecord.from_document(team_dict) for team_dict in
                self.team_dao.get_team_documents_with_grouping_with_max_count()]

    def save_dupes(self, name, team_ids):
        self.team_dao.store_dupes(name, team_ids)

    def get_unique_team_records_by_grouping(self, grouping_name):
        # type (str) -> list[TeamRecord]
        return [TeamRecord.from_document(team_dict) for team_dict in
                self.team_dao.get_unique_team_records_by_grouping(grouping_name)]
