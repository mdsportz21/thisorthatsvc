from bson import ObjectId

from model.dto import SubjectDTO, BracketDTO, RoundDTO, MatchupDTO, SlotDTO, RegionSlotDTO, MatchupSlotDTO, TeamSlotDTO, \
    TeamDTO
from model.record import SubjectRecord, Team, Bracket, Matchup, Round, Slot, TeamSlot, MatchupSlot, RegionSlot, \
    SlotConversionException


def to_subject(subject_dto):
    # type: (SubjectDTO) -> Team
    subject = Team(name=subject_dto.name,
                   description=subject_dto.description,
                   img_link=subject_dto.imgLink,
                   level=subject_dto.level,
                   affiliate=subject_dto.affiliate,
                   address=subject_dto.address)
    return subject


def to_subjects(subject_dtos):
    # type: (list[SubjectDTO]) -> list[Team]
    return [to_subject(dto) for dto in subject_dtos]


def to_subject_record(subject_dto):
    # type: (SubjectDTO) -> SubjectRecord
    subject_record = SubjectRecord(name=subject_dto.name,
                                   description=subject_dto.description,
                                   img_link=subject_dto.imgLink,
                                   level=subject_dto.level,
                                   affiliate=subject_dto.affiliate,
                                   address=subject_dto.address)
    subject_record.id = ObjectId(subject_dto.subjectId) if subject_dto.subjectId is not None else None
    return subject_record


def to_subject_records(subject_dtos):
    # type: (list[SubjectDTO]) -> list[SubjectRecord]
    return [to_subject_record(dto) for dto in subject_dtos]


def to_subject_dto(subject_record):
    # type: (SubjectRecord) -> SubjectDTO
    subject_dto = SubjectDTO(name=subject_record.name,
                             imgLink=subject_record.img_link,
                             subjectId=str(subject_record.id) if subject_record.id is not None else None)
    return subject_dto


def to_subject_dtos(subject_records):
    # type: (list[SubjectRecord]) -> list[SubjectDTO]
    return [to_subject_dto(record) for record in subject_records]


def to_team_dto(team):
    # type: (Team) -> TeamDTO
    team_dto = TeamDTO(team.name, team.description, team.img_link, team.address, team.affiliate, team.level)
    return team_dto


def to_slot_dto(slot):
    # type: (Slot) -> SlotDTO
    if isinstance(slot, TeamSlot):
        team_dto = to_team_dto(slot.team)
        return TeamSlotDTO(team_dto, slot.seed)
    if isinstance(slot, RegionSlot):
        region_dto = to_bracket_dto(slot.region)
        return RegionSlotDTO(region_dto, slot.seed)
    if isinstance(slot, MatchupSlot):
        matchup_dto = to_matchup_dto(slot.matchup)
        return MatchupSlotDTO(matchup_dto, slot.seed)
    raise SlotConversionException("Unable to convert slot to dto because unknown type for slot: " + str(slot))


def to_matchup_dto(matchup):
    # type: (Matchup) -> MatchupDTO

    slot_dto_one = to_slot_dto(matchup.slot_one)
    slot_dto_two = to_slot_dto(matchup.slot_two)
    slot_dto_winner = to_slot_dto(matchup.winner) if matchup.winner is not None else None
    matchup_dto = MatchupDTO(slot_dto_one, slot_dto_two, slot_dto_winner)
    return matchup_dto


def to_round_dto(_round):
    # type: (Round) -> RoundDTO
    matchup_dtos = [to_matchup_dto(matchup) for matchup in _round.matchups]
    round_dto = RoundDTO(matchup_dtos)
    return round_dto


def to_bracket_dto(bracket):
    # type: (Bracket) -> BracketDTO
    round_dtos = [to_round_dto(_round) for _round in bracket.rounds]
    bracket_dto = BracketDTO(rounds=round_dtos)
    return bracket_dto
