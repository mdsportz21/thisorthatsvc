

class BracketInstanceResponse():
    """
    :type bracketInstance: BracketInstanceDTO
    :type teams: list of TeamDTO
    """

    def __init__(self, bracketInstance: BracketInstanceDTO, teams: List[TeamDTO]) -> None:
        self.bracketInstance = bracketInstance
        self.teams = teams