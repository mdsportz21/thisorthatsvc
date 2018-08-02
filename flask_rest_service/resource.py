from typing import List

from bson import ObjectId

from bracket import BracketController, SeedingStrategy
from model.dto import BracketInstanceDTO, TeamDTO, BaseDTO


class BracketInstanceResponse(BaseDTO):
    """
    :type bracketInstance: BracketInstanceDTO
    :type teams: list of TeamDTO
    """

    def __init__(self, bracketInstance: BracketInstanceDTO, teams: List[TeamDTO]) -> None:
        self.bracketInstance = bracketInstance
        self.teams = teams

    def to_dict(self) -> dict:
        return dict(
            bracketInstance=self.bracketInstance.to_dict(),
            teams=[team.to_dict() for team in self.teams]
        )


class BracketResource(object):
    def __init__(self, pymongo):
        self.bracket_controller = BracketController(pymongo)

    def create_and_store_bracket_instance(self, bracket_field_id: ObjectId, seeding_strategy: SeedingStrategy,
                                          user: str) -> BracketInstanceResponse:
        # fetch bracket field from DB
        bracket_field_record = self.bracket_controller.get_bracket_field(bracket_field_id)

        bracket_instance_record = self.bracket_controller.generate_and_store_bracket_instance(bracket_field_record,
                                                                                              seeding_strategy, user)

        # translate record to DTO
        bracket_instance_dto = BracketInstanceDTO.from_record(bracket_instance_record)

        team_dtos = [TeamDTO.from_record(team_record) for team_record in bracket_field_record.team_records]

        return BracketInstanceResponse(bracket_instance_dto, team_dtos)
