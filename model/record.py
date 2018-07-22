from typing import Dict

from bson.objectid import ObjectId


class BaseRecord(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_values(self) -> tuple:
        raise NotImplementedError

    def __eq__(self, other):
        return self.get_values() == other.get_values()

    def __hash__(self):
        return hash(self.get_values())

    def __str__(self):
        return ','.join((str(value) for value in self.get_values()))


class BracketEntryRecord(BaseRecord):
    """ set winners to dict of bracket.matchup_id to None by default"""
    WinnersType = Dict[ObjectId, ObjectId]

    def __init__(self, _id: ObjectId, name: str, bracket_id: ObjectId, winners: WinnersType) -> None:
        self._id = _id
        self._name = name
        self._bracket_id = bracket_id
        self._winners = winners

    @property
    def id(self) -> ObjectId:
        return self._id

    @id.setter
    def id(self, value: ObjectId) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def bracket_id(self) -> ObjectId:
        return self._bracket_id

    @bracket_id.setter
    def bracket_id(self, value: ObjectId) -> None:
        self._bracket_id = value

    @property
    def winners(self) -> WinnersType:
        return self._winners

    @winners.setter
    def winners(self, value: WinnersType) -> None:
        self._winners = value

    def get_values(self):
        return (self.id, self.name, self.bracket_id, self.winners)


class BracketRecord(BaseRecord):
    """
    :type _round_records: list of RoundRecord
    :type _name: str
    :type _id: ObjectId
    :type _team_records: list of TeamRecord
    """

    def __init__(self, round_records, name, _id=None, team_records=list()):
        # type: (list[RoundRecord], str, ObjectId, list[TeamRecord]) -> None
        self._round_records = round_records
        self._name = name
        self._id = _id
        self._team_records = team_records

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def round_records(self):
        return self._round_records

    @round_records.setter
    def round_records(self, value):
        self._round_records = value

    @property
    def team_records(self):
        return self._team_records

    @team_records.setter
    def team_records(self, value):
        self._team_records = value

    def get_values(self):
        return (self.round_records, self.name, self.id, self.team_records)

    @staticmethod
    def factory(bracket_dict):
        # type: (dict) -> BracketRecord
        bracket = BracketRecord([], '')
        bracket.update(**bracket_dict)
        rounds = []
        for round_dict in bracket.round_records:
            rounds.append(RoundRecord.factory(round_dict))
        bracket.round_records = rounds
        return bracket


class RoundRecord(BaseRecord):
    """
    :type matchup_records: list of MatchupRecord
    """

    def __init__(self, matchup_records):
        # type: (list[MatchupRecord]) -> None
        self._matchup_records = matchup_records

    @property
    def matchup_records(self):
        return self._matchup_records

    @matchup_records.setter
    def matchup_records(self, value):
        self._matchup_records = value

    def get_values(self):
        return (self.matchup_records)

    @staticmethod
    def factory(round_dict):
        # type: (dict) -> RoundRecord
        round_record = RoundRecord(matchup_records=[])
        round_record.update(**round_dict)
        matchup_records = []
        for matchup_dict in round_record.matchup_records:
            matchup_records.append(MatchupRecord.factory(matchup_dict))
        round_record.matchup_records = matchup_records
        return round_record


class MatchupRecord(BaseRecord):
    """
    :type _id: ObjectId
    :type _team_one_id: ObjectId
    :type _team_two_id: ObjectId
    :type _region: str
    :type _source_matchup_one_id: ObjectId
    :type _source_matchup_two_id: ObjectId
    """

    def __init__(self, _id=None, team_one_id=None, team_two_id=None, region=None,
                 source_matchup_one_id=None,
                 source_matchup_two_id=None):
        # type: (ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId) -> None
        self._id = _id
        self._team_one_id = team_one_id
        self._team_two_id = team_two_id
        self._region = region
        self._source_matchup_one_id = source_matchup_one_id
        self._source_matchup_two_id = source_matchup_two_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def team_one_id(self):
        return self._team_one_id

    @team_one_id.setter
    def team_one_id(self, value):
        self._team_one_id = value

    @property
    def team_two_id(self):
        return self._team_two_id

    @team_two_id.setter
    def team_two_id(self, value):
        self._team_two_id = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def source_matchup_one_id(self):
        return self._source_matchup_one_id

    @source_matchup_one_id.setter
    def source_matchup_one_id(self, value):
        self._source_matchup_one_id = value

    @property
    def source_matchup_two_id(self):
        return self._source_matchup_two_id

    @source_matchup_two_id.setter
    def source_matchup_two_id(self, value):
        self._source_matchup_two_id = value

    def get_values(self):
        # type: (MatchupRecord) -> (ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId)
        return (self.id, self.team_one_id, self.team_two_id, self.region, self.source_matchup_one_id,
                self.source_matchup_two_id)

    @staticmethod
    def factory(matchup_record_dict):
        # type: (dict) -> MatchupRecord
        matchup_record = MatchupRecord()
        matchup_record.update(**matchup_record_dict)
        return matchup_record


class TeamRecord(BaseRecord):
    """
    :type _id: ObjectId
    :type _name: str
    :type _img_link: str
    :type _grouping: str
    :type _seed: str
    """

    def __init__(self, _id=None, name=None, img_link=None, grouping=None, seed=None):
        # type: (ObjectId, str, str, str, str) -> None
        self._id = _id
        self._name = name
        self._img_link = img_link
        self._grouping = grouping
        self._seed = seed

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, value):
        self._img_link = value

    @property
    def grouping(self):
        return self._grouping

    @grouping.setter
    def grouping(self, value):
        self._grouping = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    def get_values(self):
        # type: (TeamRecord) -> (ObjectId, str, str, str, str)
        return (self._id, self._name, self._img_link, self._grouping, self._seed)

    @staticmethod
    def factory(team_record_dict):
        # type: (dict) -> TeamRecord
        team_record = TeamRecord()
        team_record.update(**team_record_dict)
        return team_record
