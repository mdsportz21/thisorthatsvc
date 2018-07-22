from math import log, pow, floor
from random import sample

from bson import ObjectId

from model.record import BracketRecord, TeamRecord, MatchupRecord, RoundRecord


class BracketFactory(object):
    @staticmethod
    def generate_bracket(slot_records_unsorted, bracket_id, name):
        # type: (list[SlotRecord], ObjectId, str) -> BracketRecord
        round_records = []  # type: list[RoundRecord]

        slot_records = sorted(slot_records_unsorted, key=lambda slot: int(slot.seed))

        # create playin round
        matchup_records = []
        total_num_teams = len(slot_records)
        num_playin_games = int(total_num_teams - pow(2, floor(log(total_num_teams, 2))))

        if num_playin_games > 0:
            first_playin_idx = total_num_teams - num_playin_games * 2

            while first_playin_idx < len(slot_records) - 1:
                team_slot_one = slot_records.pop(first_playin_idx)
                team_slot_two = slot_records.pop()
                matchup_records.append(
                    MatchupRecord(team_one_id=team_slot_one.id, team_two_id=team_slot_two.id, _id=ObjectId()))

            assert len(matchup_records) == num_playin_games

            # Play-in Round
            round_records.append(RoundRecord(matchup_records=matchup_records))

        matchup_records = []
        playin_matchup_records = list(round_records[-1].matchup_records) if len(
            round_records) > 0 else []  # type: list[MatchupRecord]

        # create first round with remaining records
        assert (len(slot_records) + len(playin_matchup_records)) % 2 == 0

        while len(slot_records) > 0 or len(playin_matchup_records) > 0:
            team_slot_one_id = None
            team_slot_two_id = None
            source_matchup_one_id = None
            source_matchup_two_id = None

            if len(matchup_records) == 0:
                if len(slot_records) > 0:
                    team_slot_one_id = slot_records.pop(0).id
                else:
                    source_matchup_one_id = playin_matchup_records.pop(0).id

                if len(playin_matchup_records) > 0:
                    source_matchup_two_id = playin_matchup_records.pop().id
                else:
                    team_slot_two_id = slot_records.pop().id

            else:
                # n/2, where n = len(slot_records) + len(playin_matchup_records)
                n_over_2 = int(floor((len(slot_records) + len(playin_matchup_records)) / 2))
                if n_over_2 < len(slot_records):
                    slot_index = n_over_2
                    team_slot_one_id = slot_records.pop(slot_index).id
                else:
                    slot_index = n_over_2 - len(slot_records)
                    source_matchup_one_id = playin_matchup_records.pop(slot_index).id

                n_over_2 = int(floor((len(slot_records) + len(playin_matchup_records)) / 2))
                if n_over_2 < len(slot_records):
                    slot_index = n_over_2
                    team_slot_two_id = slot_records.pop(slot_index).id
                else:
                    slot_index = n_over_2 - len(slot_records)
                    source_matchup_two_id = playin_matchup_records.pop(slot_index).id

                    # TODO: make the higher seed slot one?

            matchup_records.append(MatchupRecord(team_one_id=team_slot_one_id,
                                                 team_two_id=team_slot_two_id,
                                                 source_matchup_one_id=source_matchup_one_id,
                                                 source_matchup_two_id=source_matchup_two_id,
                                                 _id=ObjectId()))

        # round one
        assert log(len(matchup_records), 2) % 1 == 0 or len(matchup_records) == 1
        round_records.append(RoundRecord(matchup_records=matchup_records))

        # while we haven't reached the finals (where there is only one matchup)
        while len(round_records[-1].matchup_records) >= 2:
            matchup_records = []
            prev_round_matchup_records = list(round_records[-1].matchup_records)

            # for matchup_one, matchup_two in prev_round_matchup_records
            prev_round_matchup_record_iter = iter(prev_round_matchup_records)
            for prev_round_matchup_one in prev_round_matchup_record_iter:
                prev_round_matchup_two = next(prev_round_matchup_record_iter)
                matchup_record = MatchupRecord(_id=ObjectId(), source_matchup_one_id=prev_round_matchup_one.id,
                                               source_matchup_two_id=prev_round_matchup_two.id)
                matchup_records.append(matchup_record)

            assert log(len(matchup_records), 2) % 1 == 0 or len(matchup_records) == 1
            round_records.append(RoundRecord(matchup_records=matchup_records))

        return BracketRecord(round_records=round_records, name=name, _id=bracket_id)

    @staticmethod
    def randomize_subjects(team_records):
        # type: (list[TeamRecord]) -> list[TeamRecord]
        return sample(team_records, len(team_records))  # type: list[TeamRecord]

    @staticmethod
    def generate_slot_records(team_records, bracket_id):
        # type: (list[TeamRecord], ObjectId) -> list[SlotRecord]
        # do i need to set an _id here??
        return [SlotRecord(team_id=team_record.id, seed=str(i + 1), bracket_id=bracket_id) for i, team_record in
                enumerate(BracketFactory.randomize_subjects(team_records))]

    @staticmethod
    def get_num_rounds(subjects):
        # type: (list[SubjectRecord]) -> int
        num_teams = len(subjects)
        # Play in games don't count as a round, so don't do ceiling
        # return int(ceil(log(num_teams, 2)))
        return int(log(num_teams, 2))

    @staticmethod
    def get_matchup(bracket_record, matchup_id):
        # type: (BracketRecord, ObjectId) -> MatchupRecord or None
        matchups_by_matchup_id = {}
        for round_record in bracket_record.round_records:
            for matchup_record in round_record.matchup_records:
                if matchup_id == matchup_record.id:
                    return matchup_record

        return None

    @staticmethod
    def clear_results(bracket_record):
        # type: (BracketRecord) -> None
        for round_record in bracket_record.round_records:
            for matchup_record in round_record.matchup_records:
                if matchup_record.source_matchup_one_id is not None:
                    matchup_record.team_one_id = None
                if matchup_record.source_matchup_two_id is not None:
                    matchup_record.team_two_id = None
                matchup_record.winner_slot_id = None

    @staticmethod
    def get_next_matchup(bracket_record, matchup_id):
        # type: (BracketRecord, ObjectId) -> MatchupRecord or None
        matchups_by_matchup_id = {}
        for round_record in bracket_record.round_records:
            for matchup_record in round_record.matchup_records:
                if matchup_id in (matchup_record.source_matchup_one_id, matchup_record.source_matchup_two_id):
                    return matchup_record

        return None

    @staticmethod
    def setWinner(bracket_record, matchup_id, winner_slot_id):
        # type: (BracketRecord, ObjectId, ObjectId) -> None

        # get matchup
        matchup_record = BracketFactory.get_matchup(bracket_record, matchup_id)

        # set winner
        matchup_record.winner_slot_id = winner_slot_id

        # get next matchup
        next_matchup_record = BracketFactory.get_next_matchup(bracket_record, matchup_id)

        # advance winner to next matchup
        if next_matchup_record is not None:
            if next_matchup_record.source_matchup_one_id == matchup_id:
                next_matchup_record.slot_one_id = winner_slot_id
            else:
                next_matchup_record.slot_two_id = winner_slot_id

    @staticmethod
    def validate(bracket_record):
        for round_record in bracket_record.round_records:
            for matchup_record in round_record.matchup_records:
                winner_slot_id = matchup_record.winner_slot_id
                slot_one_id = matchup_record.team_one_id
                slot_two_id = matchup_record.team_two_id

                if winner_slot_id is not None:
                    assert winner_slot_id in (slot_one_id, slot_two_id)

                if matchup_record.source_matchup_one_id is not None and slot_one_id is not None:
                    source_matchup_one = BracketFactory.get_matchup(bracket_record, matchup_record.source_matchup_one_id)
                    assert slot_one_id in (source_matchup_one.slot_one_id, source_matchup_one.slot_two_id)

                if matchup_record.source_matchup_two_id is not None and slot_two_id is not None:
                    source_matchup_two = BracketFactory.get_matchup(bracket_record, matchup_record.source_matchup_two_id)
                    assert slot_two_id in (source_matchup_two.slot_one_id, source_matchup_two.slot_two_id)
