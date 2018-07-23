from bson.objectid import ObjectId


class BaseRecord(object):
    # i don't remember why this is needed
    def get_values(self) -> tuple:
        raise NotImplementedError

    def __eq__(self, other):
        return self.get_values() == other.get_values()

    def __hash__(self):
        return hash(self.get_values())

    def __str__(self):
        return ','.join((str(value) for value in self.get_values()))

    def to_document(self):
        # type: () -> dict
        raise NotImplementedError

    @classmethod
    def from_document(cls, doc):
        # type: (dict) -> cls
        raise NotImplementedError


class RoundRecord(BaseRecord):
    """ Round of a bracket instance
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

    # def get_values(self):
    #     return (self.matchup_records)
    #
    # @staticmethod
    # def factory(round_dict):
    #     # type: (dict) -> RoundRecord
    #     round_record = RoundRecord(matchup_records=[])
    #     round_record.update(**round_dict)
    #     matchup_records = []
    #     for matchup_dict in round_record.matchup_records:
    #         matchup_records.append(MatchupRecord.factory(matchup_dict))
    #     round_record.matchup_records = matchup_records
    #     return round_record


class MatchupRecord(BaseRecord):
    """ Matchup in a bracket instance
    :type _id: ObjectId
    :type _team_one_id: ObjectId
    :type _team_two_id: ObjectId
    :type _region: str
    :type _source_matchup_one_id: ObjectId
    :type _source_matchup_two_id: ObjectId
    :type _winner_team_id: ObjectId
    """

    def __init__(self, _id=None, team_one_id=None, team_two_id=None, region=None,
                 source_matchup_one_id=None,
                 source_matchup_two_id=None, winner_team_id=None):
        # type: (ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId, ObjectId) -> None
        self._id = _id
        self._team_one_id = team_one_id
        self._team_two_id = team_two_id
        self._region = region
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
            region=self.region,
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
            region=doc['region'],
            source_matchup_one_id=doc['source_matchup_one_id'],
            source_matchup_two_id=doc['source_matchup_two_id'],
            winner_team_id=doc['winner_team_id']
        )

    # def get_values(self):
    #     # type: (MatchupRecord) -> (ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId)
    #     return (self.id, self.team_one_id, self.team_two_id, self.region, self.source_matchup_one_id,
    #             self.source_matchup_two_id)
    #
    # @staticmethod
    # def factory(matchup_record_dict):
    #     # type: (dict) -> MatchupRecord
    #     matchup_record = MatchupRecord()
    #     matchup_record.update(**matchup_record_dict)
    #     return matchup_record


class TeamRecord(BaseRecord):
    """ Team in a bracket field
    :type _id: ObjectId
    :type _name: str
    :type _img_link: str
    :type _grouping: str
    """

    def __init__(self, _id=None, name=None, img_link=None):
        # type: (TeamRecord, ObjectId, str, str, str) -> None
        self._id = _id
        self._name = name
        self._img_link = img_link

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

    def to_document(self):
        return dict(
            _id=self.id,
            name=self.name,
            img_link=self.img_link
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            _id=doc['_id'],
            name=doc['name'],
            img_link=doc['img_link']
        )

    # def get_values(self):
    #     # type: (TeamRecord) -> (ObjectId, str, str, str)
    #     return (self._id, self._name, self._img_link, self._grouping)

    # @staticmethod
    # def factory(team_record_dict):
    #     # type: (dict) -> TeamRecord
    #     team_record = TeamRecord()
    #     team_record.update(**team_record_dict)
    #     return team_record


class BracketFieldRecord(BaseRecord):
    """ the set of unique elements to be seeded in bracket instances

    :type _id: ObjectId
    :type _team_records: list of TeamRecord
    """

    def __init__(self, _id, name, team_records):
        # type (BracketFieldRecord, ObjectId, str, list[TeamRecord]) -> None
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

    # def get_values(self) -> tuple:
    #     return (self.id, self.team_records)


class BracketInstanceRecord(BaseRecord):
    """ a user’s attempt at filling out a bracket

    :type _id: ObjectId
    :type _round_records: list of RoundRecord
    :type _bracket_field_id: ObjectId
    """

    def __init__(self, _id, round_records, bracket_field_id):
        # type: (ObjectId, list[RoundRecord], ObjectId) -> None
        self._id = _id
        self._round_records = round_records
        self._bracket_field_id = bracket_field_id

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

    # def get_values(self):
    #     return (self.id, self.round_records, self.bracket_field_id)

    def to_document(self):
        return dict(
            _id=self.id,
            round_records=[round_record.to_document() for round_record in self.round_records],
            bracket_field_id=self.bracket_field_id
        )

    @classmethod
    def from_document(cls, doc):
        return cls(
            _id=doc['_id'],
            round_records=[RoundRecord.from_document(round_document) for round_document in doc['round_records']],
            bracket_field_id=doc['bracket_field_id']
        )
