from enum import Enum
from typing import List

from bson import ObjectId

import base
from bracket import record


class SeedingStrategy(Enum):
    RANDOM = 1
    USER = 2


# TODO: rename winnerTeamId to winningTeamId
class Matchup(base.DTO):
    """
    :type matchupId: str
    :type teamOneId: str
    :type teamTwoId: str
    :type winnerTeamId: str
    :type sourceMatchupOneId: str
    :type sourceMatchupTwoId: str
    """

    def __init__(self, matchupId: str, teamOneId: str, teamTwoId: str, winnerTeamId: str, sourceMatchupOneId: str,
                 sourceMatchupTwoId: str) -> None:
        self.matchupId = matchupId
        self.teamOneId = teamOneId
        self.teamTwoId = teamTwoId
        self.winnerTeamId = winnerTeamId
        self.sourceMatchupOneId = sourceMatchupOneId
        self.sourceMatchupTwoId = sourceMatchupTwoId

    def to_record(self) -> record.Matchup:
        return record.Matchup(
            _id=ObjectId(self.matchupId),
            team_one_id=ObjectId(self.teamOneId),
            team_two_id=ObjectId(self.teamTwoId),
            source_matchup_one_id=ObjectId(self.sourceMatchupOneId),
            source_matchup_two_id=ObjectId(self.sourceMatchupTwoId),
            winner_team_id=ObjectId(self.winnerTeamId)
        )

    @classmethod
    def from_record(cls, record: record.Matchup) -> 'Matchup':
        return cls(
            matchupId=str(record.id),
            teamOneId=str(record.team_one_id),
            teamTwoId=str(record.team_two_id),
            winnerTeamId=str(record.winner_team_id),
            sourceMatchupOneId=str(record.source_matchup_one_id),
            sourceMatchupTwoId=str(record.source_matchup_two_id)
        )

    def to_dict(self) -> dict:
        return dict(
            matchupId=self.matchupId,
            teamOneId=self.teamOneId,
            teamTwoId=self.teamTwoId,
            winnerTeamId=self.winnerTeamId,
            sourceMatchupOneId=self.sourceMatchupOneId,
            sourceMatchupTwoId=self.sourceMatchupTwoId
        )


class Round(base.DTO):
    """
    :type matchups: list of Matchup
    """

    def __init__(self, matchups: List[Matchup]) -> None:
        self.matchups = matchups

    def to_record(self) -> record.Round:
        return record.Round(
            matchups=[matchup.to_record() for matchup in self.matchups]
        )

    @classmethod
    def from_record(cls, record: record.Round) -> 'Round':
        return cls(
            matchups=[Matchup.from_record(matchup_record) for matchup_record in record.matchups]
        )

    def to_dict(self) -> dict:
        return dict(
            matchups=[matchup.to_dict() for matchup in self.matchups]
        )


class Team(base.DTO):
    """
    :type teamId: str
    :type name: str
    :type imgLink: str
    :type seed: int
    """

    def __init__(self, teamId: str, name: str, imgLink: str, seed: int) -> None:
        self.name = name
        self.imgLink = imgLink
        self.teamId = teamId
        self.seed = seed

    def to_record(self) -> record.SeededTeam:
        return record.SeededTeam(
            _id=ObjectId(self.teamId),
            name=self.name,
            img_link=self.imgLink,
            seed=self.seed
        )

    @classmethod
    def from_record(cls, record: record.SeededTeam) -> 'Team':
        # Unfortunately BracketField is used for both listing the bracket fields and displaying the bracket
        # In listing the bracket fields, the teams are unseeded
        # In displaying the bracket, the teams are seeded
        # So we need to handle both here so we don't have to create a different type here
        seed = record.seed if hasattr(record, 'seed') else None
        return cls(
            teamId=str(record.id),
            name=record.name,
            imgLink=record.img_link,
            seed=seed
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            imgLink=self.imgLink,
            teamId=self.teamId,
            seed=self.seed
        )


class BracketField(base.DTO):
    """
    :type bracketFieldId: str
    :type name: str
    :type teams: List of Team
    """

    def __init__(self, bracketFieldId: str, name: str, teams: List[Team]) -> None:
        self.bracketFieldId = bracketFieldId
        self.name = name
        self.teams = teams

    @classmethod
    def from_record(cls, record: record.BracketField) -> 'BracketField':
        return cls(
            bracketFieldId=str(record.id),
            name=record.name,
            teams=[Team.from_record(team_record) for team_record in record.teams]
        )

    def to_dict(self) -> dict:
        return dict(
            bracketFieldId=self.bracketFieldId,
            name=self.name,
            teams=[team.to_dict() for team in self.teams]
        )

# Validations on save
# 1. first round matches what is in the DB
# 2. all winners come from previous round
# How to save this to db with results
# 1. save rounds only
# TODO: add seeding hash property to BracketInstance
# this should encode the seeding used for this bracket field
class BracketInstance(base.DTO):
    """
    :type bracketInstanceId: str
    :type rounds: list of Round
    :type bracketField: BracketField
    :type user: str
    """

    def __init__(self, bracketInstanceId: str, rounds: List[Round], bracketField: BracketField, user: str) -> None:
        self.bracketInstanceId = bracketInstanceId
        self.rounds = rounds
        self.bracketField = bracketField
        self.user = user

    def to_record(self) -> record.BracketInstance:
        return record.BracketInstance(
            _id=ObjectId(self.bracketInstanceId),
            rounds=[round.to_record() for round in self.rounds],
            # bracket_field not needed since we won't be saving the bracket field from the UI
            # Instead, we should fetch it fresh from the DB
            bracket_field=None,
            user=self.user
        )

    @classmethod
    def from_record(cls, record: record.BracketInstance) -> 'BracketInstance':
        return cls(
            bracketInstanceId=str(record.id),
            rounds=[Round.from_record(round_record) for round_record in record.rounds],
            bracketField=BracketField.from_record(record.bracket_field),
            user=record.user
        )

    def to_dict(self) -> dict:
        return dict(
            bracketInstanceId=self.bracketInstanceId,
            rounds=[round.to_dict() for round in self.rounds],
            bracketField=self.bracketField.to_dict(),
            user=self.user
        )
