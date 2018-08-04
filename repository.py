# from model import codec
# from model.dto import TeamDTO
# from model.record import TeamRecord
#
# from db.storage import TeamDAO
#
#
# class TeamRepository(object):
#     """
#     :type team_dao: TeamDAO
#     """
#
#     def __init__(self, pymongo):
#         self.team_dao = TeamDAO(pymongo)
#
#     def get_team_records(self):
#         # type: () -> list[TeamRecord]
#         return [TeamRecord.from_document(team_dict) for team_dict in self.team_dao.get_team_documents()]
#
#     def get_team_record(self, team_id):
#         # type: () -> TeamRecord
#         team_record_dict = self.team_dao.get_team_document(team_id)
#         return TeamRecord.from_document(team_record_dict)
#
#     def store_team_dtos(self, team_dtos):
#         # type: (list[TeamDTO]) -> None
#         subject_records = codec.to_subject_records(team_dtos)
#         self.team_dao.store_team_records(subject_records)
#
#     def get_group_with_max_count(self):
#         return [TeamRecord.from_document(team_dict) for team_dict in
#                 self.team_dao.get_team_documents_with_grouping_with_max_count()]
#
#     def save_dupes(self, name, team_ids):
#         self.team_dao.store_dupes(name, team_ids)
#
#     def get_unique_team_records_by_grouping(self, grouping_name):
#         # type (str) -> list[TeamRecord]
#         return [TeamRecord.from_document(team_dict) for team_dict in
#                 self.team_dao.get_unique_team_records_by_grouping(grouping_name)]
