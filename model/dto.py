from typing import Type

from bson import ObjectId

from model.record import BaseRecord, RoundRecord, MatchupRecord, TeamRecord, BracketFieldRecord


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
    def from_record(cls, record):
        # type: (Type[RoundDTO], RoundRecord) -> RoundDTO
        return cls(
            matchups=[MatchupDTO.from_record(matchup_record) for matchup_record in record.matchup_records]
        )


class MatchupDTO(BaseDTO):
    """
    :type matchupId: str
    :type teamOneId: str
    :type teamTwoId: str
    :type winnerTeamId: str
    :type region: str
    :type sourceMatchupOneId: str
    :type sourceMatchupTwoId: str
    """

    def __init__(self, matchupId, teamOneId, teamTwoId, winnerTeamId, region, sourceMatchupOneId, sourceMatchupTwoId):
        # type: (MatchupDTO, str, str, str, str, str, str, str) -> None
        self.matchupId = matchupId
        self.teamOneId = teamOneId
        self.teamTwoId = teamTwoId
        self.winnerTeamId = winnerTeamId
        self.region = region
        self.sourceMatchupOneId = sourceMatchupOneId
        self.sourceMatchupTwoId = sourceMatchupTwoId

    def to_record(self):
        # type: (MatchupDTO) -> MatchupRecord
        return MatchupRecord(
            _id=ObjectId(self.matchupId),
            team_one_id=ObjectId(self.teamOneId),
            team_two_id=ObjectId(self.teamTwoId),
            region=self.region,
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
            region=record.region,
            sourceMatchupOneId=str(record.source_matchup_one_id),
            sourceMatchupTwoId=str(record.source_matchup_two_id)
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


class DupesDTO(BaseDTO):
    """
    :type name: str
    :type teams: list of TeamDTO
    """

    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
