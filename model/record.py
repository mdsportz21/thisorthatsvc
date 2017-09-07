import arrow
import six
from bson.objectid import ObjectId


class BaseRecord(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class SlotConversionException(Exception):
    pass


class Bracket(BaseRecord):
    """
    :type rounds: list of Round
    """

    def __init__(self, rounds, name):
        self._rounds = rounds
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        self._rounds = value

    def append_round(self, _round):
        self.rounds.append(_round)

    def append_empty_rounds(self, num_rounds):
        for i in range(0, num_rounds):
            self.rounds.append(Round([]))

    def __eq__(self, other):
        return self.rounds == other.rounds and self.name == other.name

    def __hash__(self):
        return hash((self.rounds, self.name))

    def __str__(self):
        return str(self.name + ": " + self.rounds)

    @staticmethod
    def factory(bracket_dict):
        """
        :type bracket_dict: dict
        :rtype: Bracket
        """
        bracket = Bracket([], '')
        bracket.update(**bracket_dict)
        rounds = []
        for round_dict in bracket.rounds:
            rounds.append(Round.factory(round_dict))
        bracket.rounds = rounds
        return bracket


class Round(BaseRecord):
    """
    :type matchups: list of Matchup
    """

    def __init__(self, matchups):
        self._matchups = matchups

    @property
    def matchups(self):
        return self._matchups

    @matchups.setter
    def matchups(self, value):
        self._matchups = value

    def get_matchup_by_seed(self, seed):
        for matchup in self.matchups:
            if matchup.contains_seed(seed):
                return matchup

            if isinstance(matchup.slot_one, MatchupSlot) and matchup.slot_one.matchup.contains_seed(seed):
                return matchup.slot_one.matchup

            if isinstance(matchup.slot_two, MatchupSlot) and matchup.slot_two.matchup.contains_seed(seed):
                return matchup.slot_two.matchup

        return None

    def __eq__(self, other):
        return self.matchups == other.matchups

    def __hash__(self):
        return hash(self.matchups)

    def __str__(self):
        return str(self.matchups)

    @staticmethod
    def factory(round_dict):
        """
        :type round_dict: dict
        :rtype: Round
        """
        round_ = Round([])
        round_.update(**round_dict)
        matchups = []
        for matchup_dict in round_.matchups:
            matchups.append(Matchup.factory(matchup_dict))
        round_.matchups = matchups
        return round_


class Matchup(BaseRecord):
    """
    :type slot_one: Slot
    :type slot_two: Slot
    :type winner: Slot  # This needs to be a slot so we have the seed as well
    """

    def __init__(self, slot_one, slot_two, winner=None):
        self._slot_one = slot_one
        self._slot_two = slot_two
        self._winner = winner
        # TODO: validate that winner is slot one or slot two

    @property
    def slot_one(self):
        return self._slot_one

    @slot_one.setter
    def slot_one(self, value):
        self._slot_one = value

    @property
    def slot_two(self):
        return self._slot_two

    @slot_two.setter
    def slot_two(self, value):
        self._slot_two = value

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    def get_slots_by_type(self, slot_type):
        # type: (type) -> list[Slot]
        matching_slots = []
        if isinstance(self.slot_one, slot_type):
            matching_slots.append(self.slot_one)
        if isinstance(self.slot_two, slot_type):
            matching_slots.append(self.slot_two)
        return matching_slots

    def contains_seed(self, seed):
        # type: (int) -> bool
        # does not include play in.
        return self.slot_one.seed == seed or self.slot_two.seed == seed

    def __eq__(self, other):
        return self.slot_one == other.slot_one and self.slot_two == other.slot_two and self.winner == other.winner

    def __hash__(self):
        return hash((self.slot_one, self.slot_two, self.winner))

    def __str__(self):
        return str(self.slot_one + " vs " + self.slot_two + " = " + self.winner)

    @staticmethod
    def factory(matchup_dict):
        """
        :type matchup_dict: dict
        :rtype: Matchup
        """
        matchup = Matchup(None, None)
        matchup.update(**matchup_dict)
        matchup.slot_one = Slot.factory(matchup.slot_one)
        matchup.slot_two = Slot.factory(matchup.slot_two)
        if matchup.winner is not None:
            matchup.winner = Team.factory(matchup.winner)
        return matchup


class Slot(BaseRecord):
    """
    :type seed: int
    """

    def __init__(self, seed):
        self._seed = seed

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    def __eq__(self, other):
        return self.seed == other.seed

    def __hash__(self):
        return hash(self.seed)

    def __str__(self):
        return str(self.seed)

    @staticmethod
    def factory(slot_dict):
        """
        :type slot_dict: dict
        :rtype: Slot
        """
        if '_team' in slot_dict:
            return TeamSlot.factory(slot_dict)
        if '_region' in slot_dict:
            return RegionSlot.factory(slot_dict)
        if '_matchup' in slot_dict:
            return MatchupSlot.factory(slot_dict)
        raise SlotConversionException('Unable to convert slot: ' + str(slot_dict))


class TeamSlot(Slot):
    """
    :type team: Team
    """

    def __init__(self, team, seed=None):
        super(TeamSlot, self).__init__(seed=seed)
        self._team = team

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    def __eq__(self, other):
        return super(TeamSlot, self).__eq__(other) and self.team == other.team

    def __hash__(self):
        return hash((self.team, super(TeamSlot, self).__hash__()))

    def __str__(self):
        return str(self.team) + ', ' + super(TeamSlot, self).__str__()

    @staticmethod
    def factory(slot_dict):
        """
        :type slot_dict: dict
        :rtype: TeamSlot
        """
        team_slot = TeamSlot(None)
        team_slot.update(**slot_dict)
        team_slot.team = Team.factory(team_slot.team)
        return team_slot


class RegionSlot(Slot):
    """
    :type region: Bracket
    """

    def __init__(self, region, seed=None):
        super(RegionSlot, self).__init__(seed=seed)
        self._region = region

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    def __eq__(self, other):
        return super(RegionSlot, self).__eq__(other) and self.region == other.region

    def __hash__(self):
        return hash((self.region, super(RegionSlot, self).__hash__()))

    def __str__(self):
        return str(self.region) + ', ' + super(RegionSlot, self).__str__()

    @staticmethod
    def factory(region_slot_dict):
        """
        :type region_slot_dict: dict
        :rtype: RegionSlot
        """
        region_slot = RegionSlot(None)
        region_slot.update(**region_slot_dict)
        region_slot.region = Bracket.factory(region_slot.region)
        return region_slot


class MatchupSlot(Slot):
    """
    :type matchup: Matchup
    """

    def __init__(self, matchup, seed=None):
        super(MatchupSlot, self).__init__(seed=seed)
        self._matchup = matchup

    @property
    def matchup(self):
        return self._matchup

    @matchup.setter
    def matchup(self, value):
        self._matchup = value

    def __eq__(self, other):
        return self.matchup == other.matchup and super(MatchupSlot, self).__eq__(other)

    def __hash__(self):
        return hash((self.matchup, super(MatchupSlot, self).__hash__()))

    def __str__(self):
        return str(self.matchup) + ', ' + super(MatchupSlot, self).__str__()

    @staticmethod
    def factory(matchup_slot_dict):
        """
        :type matchup_slot_dict: dict
        :rtype: MatchupSlot
        """
        matchup_slot = MatchupSlot(None)
        matchup_slot.update(**matchup_slot_dict)
        matchup_slot.matchup = Matchup.factory(matchup_slot.matchup)
        return matchup_slot


class InvalidSlotException(Exception):
    pass


class Victim(BaseRecord):
    """
    :type victim_id: ObjectId
    :type battle_date: arrow.Arrow
    :type explicit: bool
    """

    def __init__(self, victim_id=None, battle_date=None, explicit=None):
        self._victim_id = victim_id
        self._battle_date = battle_date
        self._explicit = explicit

    @property
    def victim_id(self):
        return self._victim_id

    @victim_id.setter
    def victim_id(self, value):
        self._victim_id = value

    @property
    def battle_date(self):
        return self._battle_date

    @battle_date.setter
    def battle_date(self, value):
        self._battle_date = value

    @property
    def explicit(self):
        return self._explicit

    @explicit.setter
    def explicit(self, value):
        self._explicit = value

    def __eq__(self, other):
        return self.victim_id == other.victim_id

    def __hash__(self):
        return hash(self.victim_id)

    def __str__(self):
        return str(self.victim_id) + ': ' + str(self._battle_date)

    @staticmethod
    def create_victim(victim_id, is_explicit=True):
        # type: (ObjectId, bool) -> Victim
        return Victim(victim_id, arrow.Arrow.utcnow(), is_explicit)

    @staticmethod
    def factory(victim_dict):
        """
        :type victim_dict: dict
        :rtype: Victim
        """
        victim = Victim()
        victim.update(**victim_dict)
        if victim.battle_date is not None and isinstance(victim.battle_date, six.string_types):
            victim.battle_date = arrow.get(victim.battle_date)
        return victim


class SubjectRecord(BaseRecord):
    """
    :type _id: ObjectId
    :type name: str
    :type description: str
    :type img_link: str
    :type victims: set of Victim
    :type address: dict[str, str]
    :type affiliate: str
    :type level: str
    """

    def __init__(self, _id=None, name=None, description=None, img_link=None, victims=None, address=None, affiliate=None,
                 level=None):
        self._level = level
        self._affiliate = affiliate
        self._address = address
        self._id = _id
        self._name = name
        self._description = description
        self._img_link = img_link
        self._victims = victims if victims is not None else set()

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
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, value):
        self._img_link = value

    @property
    def victims(self):
        return self._victims

    @victims.setter
    def victims(self, value):
        self._victims = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def affiliate(self):
        return self._affiliate

    @affiliate.setter
    def affiliate(self, value):
        self._affiliate = value

    def has_victim(self, subject_id):
        # type: (ObjectId) -> bool
        for victim in self.victims:
            if victim.victim_id == subject_id:
                return True
        return False

    def as_victim(self):
        return Victim.create_victim(self.id)

    def __eq__(self, other):
        return self._id == other.id

    def __hash__(self):
        return hash(self._id)

    @staticmethod
    def factory(subject_record_dict):
        """
        :type subject_record_dict: dict
        :rtype: SubjectRecord
        """
        subject = SubjectRecord()
        subject.update(**subject_record_dict)
        victims = set()
        for victim_dict in subject.victims:
            victims.add(Victim.factory(victim_dict))
        subject.victims = victims
        return subject


class Team(BaseRecord):
    """
    :type name: str
    :type description: str
    :type img_link: str
    :type address: dict[str, str]
    :type affiliate: str
    :type level: str
    """

    def __init__(self, name=None, description=None, img_link=None, address=None, affiliate=None, level=None):
        self._level = level
        self._affiliate = affiliate
        self._address = address
        self._name = name
        self._description = description
        self._img_link = img_link

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, value):
        self._img_link = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def affiliate(self):
        return self._affiliate

    @affiliate.setter
    def affiliate(self, value):
        self._affiliate = value

    def __eq__(self, other):
        return self.name == other.name and self.img_link == other.img_link

    def __hash__(self):
        return hash((self.name, self.img_link))

    @staticmethod
    def factory(subject_dict):
        """
        :type subject_dict: dict
        :rtype: Team
        """
        subject = Team()
        subject.update(**subject_dict)
        return subject
