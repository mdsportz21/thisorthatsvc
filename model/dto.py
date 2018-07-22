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
    :type teamOneId: str
    :type teamTwoId: str
    :type winnerTeamId: str
    :type region: str
    :type sourceMatchupOneId: str
    :type sourceMatchupTwoId: str
    """

    def __init__(self, matchupId, teamOneId, teamTwoId, winnerTeamId, region, sourceMatchupOneId, sourceMatchupTwoId):
        # type: (str, str, str, str, str, str, str) -> None
        self.matchupId = matchupId
        self.teamOneId = teamOneId
        self.teamTwoId = teamTwoId
        self.winnerTeamId = winnerTeamId
        self.region = region
        self.sourceMatchupOneId = sourceMatchupOneId
        self.sourceMatchupTwoId = sourceMatchupTwoId


# TeamDTO = TeamRecord + SlotRecord
class TeamDTO(BaseDTO):
    """
    :type teamId: str
    :type name: str
    :type imgLink: str
    :type seed: str
    """

    def __init__(self, teamId, name, seed=None, imgLink=None):
        # type: (str, str, str, str) -> None
        self.name = name
        self.imgLink = imgLink
        self.teamId = teamId
        self.seed = seed


class DupesDTO(BaseDTO):
    """
    :type name: str
    :type teams: list of TeamDTO
    """
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
