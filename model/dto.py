from typing import Type, List

from bson import ObjectId

from model.record import BaseRecord, RoundRecord, MatchupRecord, TeamRecord, BracketFieldRecord, BracketInstanceRecord


class BaseDTO(object):
    """
    """

    def to_record(self):
        # type: (BaseDTO) -> BaseRecord
        raise NotImplementedError

    @classmethod
    def from_record(cls, record):
        # type: (Type[BaseDTO], BaseRecord) -> BaseDTO
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError


class RoundDTO(BaseDTO):
    """
    :type matchups: list of MatchupDTO
    """

    def __init__(self, matchups):
        # type: (RoundDTO, list[MatchupDTO]) -> None
        self.matchups = matchups

    def to_record(self):
        # type: (RoundDTO) -> RoundRecord
        return RoundRecord(
            matchup_records=[matchup.to_record() for matchup in self.matchups]
        )

    @classmethod
    def from_record(cls, record: RoundRecord) -> 'RoundDTO':
        return cls(
            matchups=[MatchupDTO.from_record(matchup_record) for matchup_record in record.matchup_records]
        )

    def to_dict(self) -> dict:
        return dict(
            matchups=[matchup.to_dict() for matchup in self.matchups]
        )


class BracketInstanceDTO(BaseDTO):
    """
    :type rounds: list of RoundDTO
    :type bracketFieldId: str
    """

    def __init__(self, rounds: List[RoundDTO], bracketFieldId: str) -> None:
        self.rounds = rounds
        self.bracketFieldId = bracketFieldId

    def to_record(self) -> BracketInstanceRecord:
        return BracketInstanceRecord(
            _id=ObjectId(self.bracketFieldId),
            round_records=[round.to_record() for round in self.rounds]
        )

    @classmethod
    def from_record(cls, record: BracketInstanceRecord) -> 'BracketInstanceDTO':
        return cls(
            rounds=[RoundDTO.from_record(round_record) for round_record in record.round_records],
            bracketFieldId=str(record.bracket_field_id)
        )

    def to_dict(self) -> dict:
        return dict(
            rounds=[round.to_dict() for round in self.rounds],
            bracketFieldId=self.bracketFieldId
        )


class MatchupDTO(BaseDTO):
    """
    :type matchupId: str
    :type teamOneId: str
    :type teamTwoId: str
    :type winnerTeamId: str
    :type sourceMatchupOneId: str
    :type sourceMatchupTwoId: str
    """

    def __init__(self, matchupId: str, teamOneId: str, teamTwoId: str, winnerTeamId: str, sourceMatchupOneId: str,
                 sourceMatchupTwoId: str):
        # type: (MatchupDTO, str, str, str, str, str, str, str) -> None
        self.matchupId = matchupId
        self.teamOneId = teamOneId
        self.teamTwoId = teamTwoId
        self.winnerTeamId = winnerTeamId
        self.sourceMatchupOneId = sourceMatchupOneId
        self.sourceMatchupTwoId = sourceMatchupTwoId

    def to_record(self):
        # type: (MatchupDTO) -> MatchupRecord
        return MatchupRecord(
            _id=ObjectId(self.matchupId),
            team_one_id=ObjectId(self.teamOneId),
            team_two_id=ObjectId(self.teamTwoId),
            source_matchup_one_id=ObjectId(self.sourceMatchupOneId),
            source_matchup_two_id=ObjectId(self.sourceMatchupTwoId)
        )

    @classmethod
    def from_record(cls, record):
        # type: (Type(MatchupDTO), MatchupRecord) -> MatchupDTO
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


class BracketFieldDTO(BaseDTO):
    """
    :type bracketFieldId: str
    :type name: str
    :type teamCount: int
    """

    def __init__(self, bracketFieldId, name, teamCount):
        # type: (BracketFieldDTO, str, str, int) -> None
        self.bracketFieldId = bracketFieldId
        self.name = name
        self.teamCount = teamCount

    def to_record(self):
        # type: (BracketFieldDTO) -> BracketFieldRecord
        return BracketFieldRecord(
            _id=ObjectId(self.bracketFieldId),
            name=self.name
        )

    @classmethod
    def from_record(cls, record):
        # type: (Type[BracketFieldDTO], BracketFieldRecord) -> BracketFieldDTO
        return cls(
            bracketFieldId=str(record.id),
            name=record.name,
            teamCount=len(record.team_records)
        )

    def to_dict(self) -> dict:
        return dict(
            bracketFieldId=self.bracketFieldId,
            name=self.name,
            teamCount=self.teamCount
        )


# TeamDTO = TeamRecord + SlotRecord
class TeamDTO(BaseDTO):
    """
    :type teamId: str
    :type name: str
    :type imgLink: str
    """

    def __init__(self, teamId, name, imgLink=None):
        # type: (str, str, str, str) -> None
        self.name = name
        self.imgLink = imgLink
        self.teamId = teamId

    def to_record(self):
        # type: (TeamDTO) -> TeamRecord
        return TeamRecord(
            _id=ObjectId(self.teamId),
            name=self.name,
            img_link=self.imgLink
        )

    @classmethod
    def from_record(cls, record):
        # type: (Type[TeamDTO], TeamRecord) -> TeamDTO
        return cls(
            teamId=str(record.id),
            name=record.name,
            imgLink=record.img_link
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            imgLink=self.imgLink,
            teamId=self.teamId
        )


class DupesDTO(BaseDTO):
    """
    :type name: str
    :type teams: list of TeamDTO
    """

    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
