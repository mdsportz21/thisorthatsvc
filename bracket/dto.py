from enum import Enum
from typing import List

from bson import ObjectId

import base
from bracket import record


class SeedingStrategy(Enum):
    RANDOM = 1
    USER = 2


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


class BracketField(base.DTO):
    """
    :type bracketFieldId: str
    :type name: str
    :type teamCount: int
    """

    def __init__(self, bracketFieldId: str, name: str, teamCount: int) -> None:
        self.bracketFieldId = bracketFieldId
        self.name = name
        self.teamCount = teamCount

    @classmethod
    def from_record(cls, record: record.BracketField) -> 'BracketField':
        return cls(
            bracketFieldId=str(record.id),
            name=record.name,
            teamCount=len(record.teams)
        )

    def to_dict(self) -> dict:
        return dict(
            bracketFieldId=self.bracketFieldId,
            name=self.name,
            teamCount=self.teamCount
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
        return cls(
            teamId=str(record.id),
            name=record.name,
            imgLink=record.img_link,
            seed=record.seed
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            imgLink=self.imgLink,
            teamId=self.teamId,
            seed=self.seed
        )


class BracketInstance(base.DTO):
    """
    :type bracketInstanceId: str
    :type rounds: list of Round
    :type bracketFieldId: str
    :type teams: list of Team
    :type user: str
    """

    def __init__(self, bracketInstanceId: str, rounds: List[Round], bracketFieldId: str, teams: List[Team],
                 user: str) -> None:
        self.bracketInstanceId = bracketInstanceId
        self.rounds = rounds
        self.bracketFieldId = bracketFieldId
        self.teams = teams
        self.user = user

    def to_record(self) -> record.BracketInstance:
        return record.BracketInstance(
            _id=ObjectId(self.bracketInstanceId),
            bracket_field_id=ObjectId(self.bracketFieldId),
            rounds=[round.to_record() for round in self.rounds],
            teams=[team.to_record() for team in self.teams],
            user=self.user
        )

    @classmethod
    def from_record(cls, record: record.BracketInstance) -> 'BracketInstance':
        return cls(
            bracketInstanceId=str(record.id),
            rounds=[Round.from_record(round_record) for round_record in record.rounds],
            bracketFieldId=str(record.bracket_field_id),
            teams=[Team.from_record(team_record) for team_record in record.teams],
            user=record.user
        )

    def to_dict(self) -> dict:
        return dict(
            bracketInstanceId=self.bracketInstanceId,
            rounds=[round.to_dict() for round in self.rounds],
            bracketFieldId=self.bracketFieldId,
            teams=[team.to_dict() for team in self.teams],
            user=self.user
        )
