class BaseDTO(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class BracketWrapperDTO(BaseDTO):
    """
    :type bracket: BracketDTO
    :type teams: list of TeamDTO
    """

    def __init__(self, bracket, teams):
        self.bracket = bracket
        self.teams = teams


class BracketDTO(BaseDTO):
    """
    :type rounds: list of RoundDTO
    :type name: str
    """

    def __init__(self, rounds, name):
        # type: (list[RoundDTO], str) -> None
        self.rounds = rounds
        self.name = name


class RoundDTO(BaseDTO):
    """
    :type matchups: list of MatchupDTO
    """

    def __init__(self, matchups):
        # type: (list[MatchupDTO]) -> None
        self.matchups = matchups


class MatchupDTO(BaseDTO):
    """
    :type matchupId: str
    :type slotOneId: str
    :type slotTwoId: str
    :type winnerSlotId: str
    :type region: str
    :type sourceMatchupOneId: str
    :type sourceMatchupTwoId: str
    """

    def __init__(self, matchupId, slotOneId, slotTwoId, winnerSlotId, region, sourceMatchupOneId, sourceMatchupTwoId):
        # type: (str, str, str, str, str, str, str) -> None
        self.matchupId = matchupId
        self.slotOneId = slotOneId
        self.slotTwoId = slotTwoId
        self.winnerSlotId = winnerSlotId
        self.region = region
        self.sourceMatchupOneId = sourceMatchupOneId
        self.sourceMatchupTwoId = sourceMatchupTwoId


# TeamDTO = TeamRecord + SlotRecord
class TeamDTO(BaseDTO):
    """
    :type slotId: str
    :type name: str
    :type imgLink: str
    :type seed: str
    """

    def __init__(self, slotId, name, seed=None, imgLink=None):
        # type: (str, str, str, str) -> None
        self.name = name
        self.imgLink = imgLink
        self.slotId = slotId
        self.seed = seed

        # @staticmethod
        # def team_dto_factory(team_dto_dict):
        #     # type: (dict) -> TeamDTO
        #     team = TeamDTO()
        #     team.update(**team_dto_dict)
        #     if team.teamId is not None and isinstance(team.teamId, six.string_types):
        #         team.teamId = ObjectId(team.teamId)
        #     return team
