from typing import List, Dict

from bson.objectid import ObjectId


class BaseRecord(object):
    def __eq__(self, other):
        return self.get_values() == other.get_values()

    def __hash__(self):
        return hash(self.get_values())

    def __str__(self):
        return ','.join((str(value) for value in self.get_values()))

    def to_document(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def from_document(cls, doc):
        # type: (dict) -> cls
        raise NotImplementedError


class MatchupRecord(BaseRecord):
    """ Matchup in a bracket instance
    :type _id: ObjectId
    :type _team_one_id: ObjectId
    :type _team_two_id: ObjectId
    :type _source_matchup_one_id: ObjectId
    :type _source_matchup_two_id: ObjectId
    :type _winner_team_id: ObjectId
    """

    def __init__(self, _id=None, team_one_id=None, team_two_id=None, source_matchup_one_id=None,
                 source_matchup_two_id=None, winner_team_id=None):
        # type: (ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId, ObjectId) -> None
        self._id = _id
        self._team_one_id = team_one_id
        self._team_two_id = team_two_id
        self._source_matchup_one_id = source_matchup_one_id
        self._source_matchup_two_id = source_matchup_two_id
        self._winner_team_id = winner_team_id

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

    @property
    def winner_team_id(self):
        return self._winner_team_id

    @winner_team_id.setter
    def winner_team_id(self, value):
        self._winner_team_id = value

    def to_document(self):
        return dict(
            _id=self.id,
            team_one_id=self.team_one_id,
            team_two_id=self.team_two_id,
            source_matchup_one_id=self.source_matchup_one_id,
            source_matchup_two_id=self.source_matchup_two_id,
            winner_team_id=self.winner_team_id
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            _id=doc['_id'],
            team_one_id=doc['team_one_id'],
            team_two_id=doc['team_two_id'],
            source_matchup_one_id=doc['source_matchup_one_id'],
            source_matchup_two_id=doc['source_matchup_two_id'],
            winner_team_id=doc['winner_team_id']
        )


class RoundRecord(BaseRecord):
    """ Round of a bracket instance
    :type matchup_records: list of MatchupRecord
    """

    def __init__(self, matchup_records: List[MatchupRecord]) -> None:
        self._matchup_records = matchup_records

    @property
    def matchup_records(self):
        return self._matchup_records

    @matchup_records.setter
    def matchup_records(self, value):
        self._matchup_records = value

    def to_document(self):
        return dict(
            matchup_records=[matchup_record.to_document() for matchup_record in self.matchup_records]
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            matchup_records=[MatchupRecord.from_document(matchup_document) for matchup_document in
                             doc['matchup_records']]
        )


class TeamRecord(BaseRecord):
    """ Team in a bracket field
    :type _id: ObjectId
    :type _name: str
    :type _img_link: str
    :type _grouping: str
    :type _seed: int
    """

    def __init__(self, _id=None, name=None, img_link=None, seed=None):
        # type: (TeamRecord, ObjectId, str, str, str, int) -> None
        self._id = _id
        self._name = name
        self._img_link = img_link
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
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    def to_document(self):
        return dict(
            _id=self.id,
            name=self.name,
            img_link=self.img_link,
            seed=self.seed
        )

    @classmethod
    def from_document(cls, doc):
        seed = doc['seed'] if 'seed' in doc else None
        return cls(
            _id=doc['_id'],
            name=doc['name'],
            img_link=doc['img_link'],
            seed=seed
        )


class BracketFieldRecord(BaseRecord):
    """ the set of unique elements to be seeded in bracket instances

    :type _id: ObjectId
    :type _team_records: list of TeamRecord
    """

    def __init__(self, _id, name, team_records):
        # type: (BracketFieldRecord, ObjectId, str, list[TeamRecord]) -> None
        self._id = _id
        self._name = name
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
    def team_records(self):
        return self._team_records

    @team_records.setter
    def team_records(self, value):
        self._team_records = value

    def to_document(self):
        return dict(
            _id=self.id,
            name=self.name,
            team_records=[team_record.to_document() for team_record in self.team_records]
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            _id=doc['_id'],
            name=doc['name'],
            team_records=[TeamRecord.from_document(team_document) for team_document in doc['team_records']]
        )


class BracketInstanceRecord(BaseRecord):
    """ a user’s attempt at filling out a bracket

    :type _id: ObjectId
    :type _round_records: list of RoundRecord
    :type _bracket_field_id: ObjectId
    :type _user: str
    """

    def __init__(self, _id, round_records, bracket_field_id=None, user=None):
        # type: (ObjectId, list[RoundRecord], ObjectId) -> None
        self._id = _id
        self._round_records = round_records
        self._bracket_field_id = bracket_field_id
        self._user = user

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def round_records(self):
        return self._round_records

    @round_records.setter
    def round_records(self, value):
        self._round_records = value

    @property
    def bracket_field_id(self):
        return self._bracket_field_id

    @bracket_field_id.setter
    def bracket_field_id(self, value):
        self._bracket_field_id = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def to_document(self):
        return dict(
            _id=self.id,
            round_records=[round_record.to_document() for round_record in self.round_records],
            bracket_field_id=self.bracket_field_id,
            user=self.user
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            _id=doc['_id'],
            round_records=[RoundRecord.from_document(round_document) for round_document in doc['round_records']],
            bracket_field_id=doc['bracket_field_id'],
            user=doc['user']
        )
