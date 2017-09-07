import six
from bson.objectid import ObjectId

from model.record import SubjectRecord


class BaseDTO(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class SubjectDTO(BaseDTO):
    """
    :type subjectId: ObjectId
    :type name: str
    :type description: str
    :type imgLink: str
    :type selected: bool
    :type address: dict[str, str]
    :type affiliate: str
    :type level: str
    """

    def __init__(self, subjectId=None, name=None, description=None, imgLink=None, selected=None, tags=None,
                 address=None, affiliate=None, level=None):
        # type: (ObjectId, str, str, str, bool, dict[str, str], str, str) -> None
        self.level = level
        self.affiliate = affiliate
        self.address = address
        self.tags = tags
        self.subjectId = subjectId
        self.name = name
        self.description = description
        self.imgLink = imgLink
        self.selected = selected

    @staticmethod
    def subject_dto_factory(subject_dto_dict):
        # type: (dict) -> SubjectDTO
        subject = SubjectDTO()
        subject.update(**subject_dto_dict)
        if subject.subjectId is not None and isinstance(subject.subjectId, six.string_types):
            subject.subjectId = ObjectId(subject.subjectId)
        return subject


class RankingDTO(BaseDTO):
    """
    :type subjectId: ObjectId
    :type name: str
    :type description: str
    :type imgLink: str
    :type rank: int
    :type victims: list of ObjectId
    :type wins: int
    :type faced: int
    """

    def __init__(self, subject_id=None, name=None, description=None, img_link=None, rank=None, victims=None, wins=0,
                 faced=0):
        # type: (ObjectId, str, str, str, int, list[ObjectId], int, int) -> None
        self.subjectId = subject_id
        self.name = name
        self.description = description
        self.imgLink = img_link
        self.rank = rank
        self.victims = victims
        self.wins = wins
        self.faced = faced

    @staticmethod
    def to_ranking_dto(subject_record, rank):
        # type: (SubjectRecord, int) -> RankingDTO
        victims = [str(victim.victim_id) for victim in subject_record.victims]
        ranking_dto = RankingDTO(subject_id=str(subject_record.id), name=subject_record.name,
                                 description=subject_record.description,
                                 img_link=subject_record.img_link, rank=rank,
                                 victims=victims)
        return ranking_dto


class BracketDTO(BaseDTO):
    """
    :type rounds: list of RoundDTO
    """

    def __init__(self, rounds):
        # type: (list[RoundDTO]) -> None
        self.rounds = rounds


class RoundDTO(BaseDTO):
    """
    :type matchups: list of MatchupDTO
    """

    def __init__(self, matchups):
        # type: (list[MatchupDTO]) -> None
        self.matchups = matchups


class MatchupDTO(BaseDTO):
    """
    :type slotOne: SlotDTO
    :type slotTwo: SlotDTO
    :type winner: SlotDTO
    """

    def __init__(self, slotOne, slotTwo, winner):
        # type: (SlotDTO, SlotDTO, SlotDTO) -> None
        self.slotOne = slotOne
        self.slotTwo = slotTwo
        self.winner = winner


class SlotDTO(BaseDTO):
    """
    :type seed: int
    """

    def __init__(self, seed):
        # type: (int) -> None
        self.seed = seed


class TeamDTO(BaseDTO):
    """
    :type name: str
    :type description: str
    :type img_link: str
    :type address: dict[str, str]
    :type affiliate: str
    :type level: str
    """

    def __init__(self, name, description, img_link, address, affiliate, level):
        # type: (str, str, str, dict[str, str], str, str) -> None
        self.name = name
        self.description = description
        self.img_link = img_link
        self.address = address
        self.affiliate = affiliate
        self.level = level


class TeamSlotDTO(SlotDTO):
    """
    :type team: SubjectDTO
    """

    def __init__(self, team, seed):
        # type: (TeamDTO, int) -> None
        super(TeamSlotDTO, self).__init__(seed=seed)
        self.team = team


class RegionSlotDTO(SlotDTO):
    """
    :type region: BracketDTO
    """

    def __init__(self, region, seed):
        # type: (BracketDTO, int) -> None
        super(RegionSlotDTO, self).__init__(seed=seed)
        self.region = region


class MatchupSlotDTO(SlotDTO):
    """
    :type matchup: MatchupDTO
    """

    def __init__(self, matchup, seed):
        # type: (MatchupDTO, int) -> None
        super(MatchupSlotDTO, self).__init__(seed=seed)
        self.matchup = matchup
