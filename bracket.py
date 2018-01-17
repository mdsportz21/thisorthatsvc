from math import log, pow, floor
from random import sample

from bson import ObjectId

from model.record import BracketRecord, TeamRecord, SlotRecord, MatchupRecord, RoundRecord


class BracketFactory(object):
    @staticmethod
    def generate_bracket(slot_records_unsorted, bracket_id, name):
        # type: (list[SlotRecord], ObjectId, str) -> BracketRecord
        round_records = []  # type: list[RoundRecord]

        slot_records = sorted(slot_records_unsorted, key=lambda slot: slot.seed)

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
                    MatchupRecord(slot_one_id=team_slot_one.id, slot_two_id=team_slot_two.id, _id=ObjectId()))

            assert len(matchup_records) == num_playin_games

            # Play-in Round
            round_records.append(RoundRecord(matchup_records=matchup_records))

        matchup_records = []
        playin_matchup_records = list(round_records[-1].matchup_records) if len(
            round_records) > 0 else []  # type: list[MatchupRecord]

        # create first round with remaining records
        while len(slot_records) > 0:
            team_slot_one_id = slot_records.pop(0).id
            team_slot_two_id = None
            source_matchup_id = None

            if len(playin_matchup_records) > 0:
                playin_matchup_record = playin_matchup_records.pop()
                source_matchup_id = playin_matchup_record.id
            else:
                team_slot_two_id = slot_records.pop().id

            matchup_records.append(MatchupRecord(slot_one_id=team_slot_one_id, slot_two_id=team_slot_two_id,
                                                 source_matchup_two_id=source_matchup_id, _id=ObjectId()))

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
