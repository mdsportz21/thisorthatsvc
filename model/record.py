from bson.objectid import ObjectId


class BaseRecord(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class BracketRecord(BaseRecord):
    """
    :type _round_records: list of RoundRecord
    :type _name: str
    :type _id: ObjectId
    """

    def __init__(self, round_records, name, _id=None):
        # type: (list[RoundRecord], str) -> None
        self._round_records = round_records
        self._name = name
        self._id = _id

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

    def __eq__(self, other):
        return self.round_records == other.round_records and \
               self.name == other.name

    def __hash__(self):
        return hash((self.round_records, self.name))

    def __str__(self):
        return str(self.name + ": " + str(self.round_records))

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

    def __eq__(self, other):
        return self.matchup_records == other.matchup_records

    def __hash__(self):
        return hash(self.matchup_records)

    def __str__(self):
        return str(self.matchup_records)

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
    :type _slot_one_id: ObjectId
    :type _slot_two_id: ObjectId
    :type _winner_slot_id: ObjectId  # This needs to be a slot so we have the seed as well
    :type _region: str
    :type _source_matchup_one_id: ObjectId
    :type _source_matchup_two_id: ObjectId
    """

    def __init__(self, _id=None, slot_one_id=None, slot_two_id=None, winner_slot_id=None, region=None,
                 source_matchup_one_id=None,
                 source_matchup_two_id=None):
        # type: (ObjectId, ObjectId, ObjectId, ObjectId, str, ObjectId, ObjectId) -> None
        self._id = _id
        self._slot_one_id = slot_one_id
        self._slot_two_id = slot_two_id
        self._winner_slot_id = winner_slot_id
        self._region = region
        self._source_matchup_one_id = source_matchup_one_id
        self._source_matchup_two_id = source_matchup_two_id

        # TODO: validate that slot one comes from matchup one
        # TODO: validate that slot two comes from matchup two

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def slot_one_id(self):
        return self._slot_one_id

    @slot_one_id.setter
    def slot_one_id(self, value):
        self._slot_one_id = value

    @property
    def slot_two_id(self):
        return self._slot_two_id

    @slot_two_id.setter
    def slot_two_id(self, value):
        self._slot_two_id = value

    @property
    def winner_slot_id(self):
        return self._winner_slot_id

    @winner_slot_id.setter
    def winner_slot_id(self, value):
        # if value is not None:
        #     assert value == self.slot_one_id or value == self.slot_two_id
        self._winner_slot_id = value

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

    def __eq__(self, other):
        return self.slot_one_id == other.slot_one_id \
               and self.slot_two_id == other.slot_two_id \
               and self.region == other.region

    def __hash__(self):
        return hash((self.slot_one_id, self.slot_two_id, self.region))

    def __str__(self):
        return self.region + ": " + str(self.slot_one_id) + " vs " + str(self.slot_two_id) + " => " + str(
            self.winner_slot_id)

    @staticmethod
    def factory(matchup_record_dict):
        # type: (dict) -> MatchupRecord
        matchup_record = MatchupRecord()
        matchup_record.update(**matchup_record_dict)
        return matchup_record


class SlotRecord(BaseRecord):
    """
    :type _team_id: ObjectId
    :type _seed: str
    :type _bracket_id: ObjectId
    :type _id: ObjectId
    """

    def __init__(self, team_id=None, seed=None, bracket_id=None, _id=None):
        # type: (ObjectId, str, ObjectId, ObjectId) -> None
        self._id = _id
        self._team_id = team_id
        self._seed = seed
        self._bracket_id = bracket_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, value):
        self._team_id = value

    @property
    def bracket_id(self):
        return self._bracket_id

    @bracket_id.setter
    def bracket_id(self, value):
        self._bracket_id = value

    def __eq__(self, other):
        return self.team_id == other.team_id \
               and self.seed == other.seed \
               and self.bracket_id == other.bracket_id

    def __hash__(self):
        return hash((self.team_id, self.seed, self.bracket_id))

    def __str__(self):
        return ','.join((str(self.team_id), str(self.seed), str(self.bracket_id)))

    @staticmethod
    def factory(slot_record_dict):
        # type: (dict) -> SlotRecord
        slot_record = SlotRecord()
        slot_record.update(**slot_record_dict)
        return slot_record


class TeamRecord(BaseRecord):
    """
    :type _id: ObjectId
    :type _name: str
    :type _img_link: str
    """

    def __init__(self, _id=None, name=None, img_link=None):
        # type: (ObjectId, str, str)
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

    @staticmethod
    def factory(team_record_dict):
        # type: (dict) -> TeamRecord
        team_record = TeamRecord()
        team_record.update(**team_record_dict)
        return team_record
