from model.dto import RoundDTO, MatchupDTO, TeamDTO
from model.record import TeamRecord, RoundRecord, MatchupRecord


# I think ObjectId works better as a string, otherwise I keep getting:
#   AttributeError: 'ObjectId' object has no attribute '_'
# subject_record.id = ObjectId(subject_dto.subjectId) if subject_dto.subjectId is not None else None


def to_team_dtos(team_records):
    # type: (list[TeamRecord]) -> list[TeamDTO]
    return [to_team_dto(team_record) for team_record in team_records]


def to_team_dto(team_record):
    # type: (TeamRecord) -> TeamDTO
    return TeamDTO(teamId=str(team_record._id),
                   name=team_record.name,
                   imgLink=team_record.img_link)


def to_round_dtos(round_records):
    # type: (list[RoundRecord]) -> list[RoundDTO]
    return [to_round_dto(round_record) for round_record in round_records]


def to_round_dto(round_record):
    # type: (RoundRecord) -> RoundDTO
    return RoundDTO(matchups=to_matchup_dtos(round_record.matchup_records))


def to_matchup_dtos(matchup_records):
    # type: (list[MatchupRecord]) -> list[MatchupDTO]
    return [to_matchup_dto(matchup_record) for matchup_record in matchup_records]


def to_matchup_dto(matchup_record):
    # type: (MatchupRecord) -> MatchupDTO
    return MatchupDTO(matchupId=str(matchup_record.id),
                      slotOneId=str(matchup_record.team_one_id),
                      slotTwoId=str(matchup_record.team_two_id),
                      winnerSlotId=str(matchup_record.winner_slot_id),
                      region=matchup_record.region,
                      sourceMatchupOneId=str(matchup_record.source_matchup_one_id),
                      sourceMatchupTwoId=str(matchup_record.source_matchup_two_id))
