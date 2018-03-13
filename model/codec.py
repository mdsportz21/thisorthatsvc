from model.dto import BracketDTO, RoundDTO, MatchupDTO, TeamDTO
from model.record import BracketRecord, TeamRecord, SlotRecord, RoundRecord, MatchupRecord


# I think ObjectId works better as a string, otherwise I keep getting:
#   AttributeError: 'ObjectId' object has no attribute '_'
# subject_record.id = ObjectId(subject_dto.subjectId) if subject_dto.subjectId is not None else None

def to_team_dtos(team_records, slot_records):
    # type: (list[TeamRecord], list[SlotRecord]) -> list[TeamDTO]
    return [to_team_dto(team_record, slot_record) for team_record, slot_record in zip(team_records, slot_records)]

def to_team_dto(team_record, slot_record):
    # type: (TeamRecord, SlotRecord) -> TeamDTO
    return TeamDTO(slotId=str(slot_record.id),
                   name=team_record.name,
                   seed=slot_record.seed,
                   imgLink=team_record.img_link)

def to_bracket_dto(bracket_record):
    # type: (BracketRecord) -> BracketDTO
    return BracketDTO(rounds=to_round_dtos(bracket_record.round_records),
                      name=bracket_record.name)

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
                      slotOneId=str(matchup_record.slot_one_id),
                      slotTwoId=str(matchup_record.slot_two_id),
                      winnerSlotId=str(matchup_record.winner_slot_id),
                      region=matchup_record.region,
                      sourceMatchupOneId=str(matchup_record.source_matchup_one_id),
                      sourceMatchupTwoId=str(matchup_record.source_matchup_two_id))