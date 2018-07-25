from enum import Enum
from math import floor, log
from random import shuffle
from typing import List

from bson import ObjectId

from model.record import TeamRecord, BracketInstanceRecord, RoundRecord, MatchupRecord
from repository import BracketRepository


class SeedingStrategy(Enum):
    RANDOM = 1
    USER = 2


class BracketController(object):
    def __init__(self, pymongo):
        self.bracket_repository = BracketRepository(pymongo)

    def generate_bracket_instance(self, bracket_field_id, seeding_strategy, user):
        # type: (BracketController, ObjectId, SeedingStrategy, str) -> None

        # fetch bracket field from DB
        bracket_field_record = self.bracket_repository.fetch_bracket_field_by_id(bracket_field_id)

        # generate the bracket from the field teams
        bracket_instance_record = BracketFactory.generate_bracket_instance(bracket_field_record.team_records,
                                                                           seeding_strategy,
                                                                           bracket_field_id,
                                                                           user)


class BracketFactory(object):
    @staticmethod
    def generate_bracket_instance(team_records, seeding_strategy, bracket_field_id, user):
        # type: (list[TeamRecord], SeedingStrategy, ObjectId, str) -> BracketInstanceRecord

        # order the field according to the seeding strategy
        if seeding_strategy == SeedingStrategy.RANDOM:
            shuffle(team_records)
        elif seeding_strategy == SeedingStrategy.USER:
            # TODO: order by highest avg finish
            pass

        round_records = BracketFactory.generate_rounds(tuple(team_records))

        # create the bracket by modifying the logic below
        bracket_instance_id = ObjectId()
        return BracketInstanceRecord(bracket_instance_id, round_records, bracket_field_id, user)

    @staticmethod
    def get_num_play_in_games(num_teams):
        # type: (int) -> int
        # examples:
        #   int(7 - 2^floor(log(7,2))) = int(7 - 2^2) = 3
        #   int(9 - 2^floor(log(9,2))) = int(9 - 2^3) = 1
        return int(num_teams - pow(2, floor(log(num_teams, 2))))

    @staticmethod
    def get_last_team_bye_index(num_teams: int, num_play_in_games: int) -> int:
        return num_teams - num_play_in_games * 2

    @staticmethod
    def generate_play_in_round(team_records_final, num_play_in_games):
        # type: (tuple[TeamRecord], int) -> RoundRecord
        matchup_records = []  # type: list[MatchupRecord]
        team_records = list(team_records_final)
        num_teams = len(team_records)

        # the play-in round should only have the last num_play_in_games * 2 teams in it
        play_in_index = BracketFactory.get_last_team_bye_index(num_teams, num_play_in_games)

        # match the team at play_in_index against the last seeded team remaining
        while play_in_index < num_teams - 1:
            team_one = team_records.pop(play_in_index)
            team_two = team_records.pop()
            matchup_record = MatchupRecord(
                _id=ObjectId(),
                team_one_id=team_one.id,
                team_two_id=team_two.id
            )
            matchup_records.append(matchup_record)
            # since we're popping records, we don't need to increment the index

        assert len(matchup_records) == num_play_in_games

        return RoundRecord(matchup_records)

    @staticmethod
    def get_middle_seed_index(unassigned_team_records: List[TeamRecord],
                              play_in_matchup_records: List[MatchupRecord]) -> int:
        # used to determine whether middle matchup comes from unassigned teams or play-in matchups
        return int(floor((len(unassigned_team_records) + len(play_in_matchup_records)) / 2))

    @staticmethod
    def generate_first_round(unassigned_team_records_final, play_in_matchup_records_final):
        # type: (tuple[TeamRecord], tuple[MatchupRecord]) -> RoundRecord
        unassigned_team_records = list(unassigned_team_records_final)
        play_in_matchup_records = list(play_in_matchup_records_final)

        # teams in first round + play-in games = power of 2
        assert (len(unassigned_team_records) + len(play_in_matchup_records)) % 2 == 0

        matchup_records: List[MatchupRecord] = []

        while not unassigned_team_records or not play_in_matchup_records:
            team_one_id = None
            team_two_id = None
            source_matchup_one_id = None
            source_matchup_two_id = None

            if matchup_records:
                # build round from middle out
                middle_seed_index = BracketFactory.get_middle_seed_index(unassigned_team_records,
                                                                         play_in_matchup_records)
                if middle_seed_index < len(unassigned_team_records):
                    # the top seed comes from team_records
                    team_index = middle_seed_index
                    team_one_id = unassigned_team_records.pop(team_index).id
                else:
                    matchup_index = middle_seed_index - len(unassigned_team_records)
                    source_matchup_one_id = play_in_matchup_records.pop(matchup_index).id

                # recalculate, since we popped
                middle_seed_index = BracketFactory.get_middle_seed_index(unassigned_team_records,
                                                                         play_in_matchup_records)
                if middle_seed_index < len(unassigned_team_records):
                    team_index = middle_seed_index
                    team_two_id = unassigned_team_records.pop(team_index).id
                else:
                    matchup_index = middle_seed_index - len(unassigned_team_records)
                    source_matchup_two_id = play_in_matchup_records.pop(matchup_index).id

            else:
                # build round from outside in
                if unassigned_team_records:
                    team_one_id = unassigned_team_records.pop(0).id
                else:
                    source_matchup_one_id = play_in_matchup_records.pop(0).id

                if play_in_matchup_records:
                    source_matchup_two_id = play_in_matchup_records.pop().id
                else:
                    team_two_id = unassigned_team_records.pop().id

            matchup_record = MatchupRecord(
                _id=ObjectId(),
                team_one_id=team_one_id,
                team_two_id=team_two_id,
                source_matchup_one_id=source_matchup_one_id,
                source_matchup_two_id=source_matchup_two_id
            )

        round_record = BracketFactory.validate_non_play_in_round(matchup_records)
        return round_record

    @staticmethod
    def validate_non_play_in_round(matchup_records: List[MatchupRecord]) -> RoundRecord:
        # number of matchups in each non-play-in round should be a power of 2
        assert log(len(matchup_records), 2) % 1 == 0
        return RoundRecord(matchup_records)

    @staticmethod
    def create_next_round(prev_round_matchup_records: tuple[MatchupRecord]) -> RoundRecord:
        prev_round_matchup_record_iter = iter(prev_round_matchup_records)
        matchup_records = []
        for prev_round_matchup_one in prev_round_matchup_record_iter:
            prev_round_matchup_two = next(prev_round_matchup_record_iter)
            matchup_record = MatchupRecord(
                _id=ObjectId(),
                source_matchup_one_id=prev_round_matchup_one.id,
                source_matchup_two_id=prev_round_matchup_two.id
            )
            matchup_records.append(matchup_record)

        round_record = BracketFactory.validate_non_play_in_round(matchup_records)
        return round_record

    @staticmethod
    def generate_rounds(team_records_final):
        # type: (tuple[TeamRecord]) -> list[RoundRecord]
        round_records: List[RoundRecord] = []
        # the teams that haven't been assigned to a round
        unassigned_team_records = list(team_records_final)

        # add seeds to teams
        for i, team in enumerate(unassigned_team_records):
            team.seed = i + 1

        # create play-in round
        matchup_records: List[MatchupRecord] = []
        num_teams = len(unassigned_team_records)
        num_play_in_games = BracketFactory.get_num_play_in_games(num_teams)

        if num_play_in_games > 0:
            play_in_round = BracketFactory.generate_play_in_round(tuple(unassigned_team_records), num_play_in_games)
            round_records.append(play_in_round)
            play_in_matchup_records = tuple(play_in_round.matchup_records)
        else:
            play_in_matchup_records: tuple[MatchupRecord] = tuple()

        # the play-in teams are in the play-in round, so we can remove them from the teams list
        last_team_bye_index = BracketFactory.get_last_team_bye_index(num_teams, num_play_in_games)
        unassigned_team_records = unassigned_team_records[:last_team_bye_index]

        first_round = BracketFactory.generate_first_round(tuple(unassigned_team_records), play_in_matchup_records)
        round_records.append(first_round)

        while len(round_records[-1].matchup_records) > 1:
            latest_round_record = BracketFactory.create_next_round(tuple(round_records[-1].matchup_records))
            round_records.append(latest_round_record)

        return round_records

    # @staticmethod
    # def generate_bracket(slot_records_unsorted, bracket_id, name):
    #     # type: (list[SlotRecord], ObjectId, str) -> BracketRecord
    #     round_records = []  # type: list[RoundRecord]
    #
    #     slot_records = sorted(slot_records_unsorted, key=lambda slot: int(slot.seed))
    #
    #     # create playin round
    #     matchup_records = []
    #     total_num_teams = len(slot_records)
    #     num_playin_games = int(total_num_teams - pow(2, floor(log(total_num_teams, 2))))
    #
    #     if num_playin_games > 0:
    #         first_playin_idx = total_num_teams - num_playin_games * 2
    #
    #         while first_playin_idx < len(slot_records) - 1:
    #             team_slot_one = slot_records.pop(first_playin_idx)
    #             team_slot_two = slot_records.pop()
    #             matchup_records.append(
    #                 MatchupRecord(team_one_id=team_slot_one.id, team_two_id=team_slot_two.id, _id=ObjectId()))
    #
    #         assert len(matchup_records) == num_playin_games
    #
    #         # Play-in Round
    #         round_records.append(RoundRecord(matchup_records=matchup_records))
    #
    #     matchup_records = []
    #     playin_matchup_records = list(round_records[-1].matchup_records) if len(
    #         round_records) > 0 else []  # type: list[MatchupRecord]
    #
    #     # create first round with remaining records
    #     assert (len(slot_records) + len(playin_matchup_records)) % 2 == 0
    #
    #     while len(slot_records) > 0 or len(playin_matchup_records) > 0:
    #         team_slot_one_id = None
    #         team_slot_two_id = None
    #         source_matchup_one_id = None
    #         source_matchup_two_id = None
    #
    #         if len(matchup_records) == 0:
    #             if len(slot_records) > 0:
    #                 team_slot_one_id = slot_records.pop(0).id
    #             else:
    #                 source_matchup_one_id = playin_matchup_records.pop(0).id
    #
    #             if len(playin_matchup_records) > 0:
    #                 source_matchup_two_id = playin_matchup_records.pop().id
    #             else:
    #                 team_slot_two_id = slot_records.pop().id
    #
    #         else:
    #             # n/2, where n = len(slot_records) + len(playin_matchup_records)
    #             n_over_2 = int(floor((len(slot_records) + len(playin_matchup_records)) / 2))
    #             if n_over_2 < len(slot_records):
    #                 slot_index = n_over_2
    #                 team_slot_one_id = slot_records.pop(slot_index).id
    #             else:
    #                 slot_index = n_over_2 - len(slot_records)
    #                 source_matchup_one_id = playin_matchup_records.pop(slot_index).id
    #
    #             n_over_2 = int(floor((len(slot_records) + len(playin_matchup_records)) / 2))
    #             if n_over_2 < len(slot_records):
    #                 slot_index = n_over_2
    #                 team_slot_two_id = slot_records.pop(slot_index).id
    #             else:
    #                 slot_index = n_over_2 - len(slot_records)
    #                 source_matchup_two_id = playin_matchup_records.pop(slot_index).id
    #
    #                 # TODO: make the higher seed slot one?
    #
    #         matchup_records.append(MatchupRecord(team_one_id=team_slot_one_id,
    #                                              team_two_id=team_slot_two_id,
    #                                              source_matchup_one_id=source_matchup_one_id,
    #                                              source_matchup_two_id=source_matchup_two_id,
    #                                              _id=ObjectId()))
    #
    #     # round one
    #     assert log(len(matchup_records), 2) % 1 == 0 or len(matchup_records) == 1
    #     round_records.append(RoundRecord(matchup_records=matchup_records))
    #
    #     # while we haven't reached the finals (where there is only one matchup)
    #     while len(round_records[-1].matchup_records) >= 2:
    #         matchup_records = []
    #         prev_round_matchup_records = list(round_records[-1].matchup_records)
    #
    #         # for matchup_one, matchup_two in prev_round_matchup_records
    #         prev_round_matchup_record_iter = iter(prev_round_matchup_records)
    #         for prev_round_matchup_one in prev_round_matchup_record_iter:
    #             prev_round_matchup_two = next(prev_round_matchup_record_iter)
    #             matchup_record = MatchupRecord(_id=ObjectId(), source_matchup_one_id=prev_round_matchup_one.id,
    #                                            source_matchup_two_id=prev_round_matchup_two.id)
    #             matchup_records.append(matchup_record)
    #
    #         assert log(len(matchup_records), 2) % 1 == 0 or len(matchup_records) == 1
    #         round_records.append(RoundRecord(matchup_records=matchup_records))
    #
    #     return BracketRecord(round_records=round_records, name=name, _id=bracket_id)
    #
    # @staticmethod
    # def randomize_subjects(team_records):
    #     # type: (list[TeamRecord]) -> list[TeamRecord]
    #     return sample(team_records, len(team_records))  # type: list[TeamRecord]
    #
    # @staticmethod
    # def generate_slot_records(team_records, bracket_id):
    #     # type: (list[TeamRecord], ObjectId) -> list[SlotRecord]
    #     # do i need to set an _id here??
    #     return [SlotRecord(team_id=team_record.id, seed=str(i + 1), bracket_id=bracket_id) for i, team_record in
    #             enumerate(BracketFactory.randomize_subjects(team_records))]
    #
    # @staticmethod
    # def get_num_rounds(subjects):
    #     # type: (list[SubjectRecord]) -> int
    #     num_teams = len(subjects)
    #     # Play in games don't count as a round, so don't do ceiling
    #     # return int(ceil(log(num_teams, 2)))
    #     return int(log(num_teams, 2))
    #
    # @staticmethod
    # def get_matchup(bracket_record, matchup_id):
    #     # type: (BracketRecord, ObjectId) -> MatchupRecord or None
    #     matchups_by_matchup_id = {}
    #     for round_record in bracket_record.round_records:
    #         for matchup_record in round_record.matchup_records:
    #             if matchup_id == matchup_record.id:
    #                 return matchup_record
    #
    #     return None
    #
    # @staticmethod
    # def clear_results(bracket_record):
    #     # type: (BracketRecord) -> None
    #     for round_record in bracket_record.round_records:
    #         for matchup_record in round_record.matchup_records:
    #             if matchup_record.source_matchup_one_id is not None:
    #                 matchup_record.team_one_id = None
    #             if matchup_record.source_matchup_two_id is not None:
    #                 matchup_record.team_two_id = None
    #             matchup_record.winner_slot_id = None
    #
    # @staticmethod
    # def get_next_matchup(bracket_record, matchup_id):
    #     # type: (BracketRecord, ObjectId) -> MatchupRecord or None
    #     matchups_by_matchup_id = {}
    #     for round_record in bracket_record.round_records:
    #         for matchup_record in round_record.matchup_records:
    #             if matchup_id in (matchup_record.source_matchup_one_id, matchup_record.source_matchup_two_id):
    #                 return matchup_record
    #
    #     return None
    #
    # @staticmethod
    # def setWinner(bracket_record, matchup_id, winner_slot_id):
    #     # type: (BracketRecord, ObjectId, ObjectId) -> None
    #
    #     # get matchup
    #     matchup_record = BracketFactory.get_matchup(bracket_record, matchup_id)
    #
    #     # set winner
    #     matchup_record.winner_slot_id = winner_slot_id
    #
    #     # get next matchup
    #     next_matchup_record = BracketFactory.get_next_matchup(bracket_record, matchup_id)
    #
    #     # advance winner to next matchup
    #     if next_matchup_record is not None:
    #         if next_matchup_record.source_matchup_one_id == matchup_id:
    #             next_matchup_record.slot_one_id = winner_slot_id
    #         else:
    #             next_matchup_record.slot_two_id = winner_slot_id
    #
    # @staticmethod
    # def validate(bracket_record):
    #     for round_record in bracket_record.round_records:
    #         for matchup_record in round_record.matchup_records:
    #             winner_slot_id = matchup_record.winner_slot_id
    #             slot_one_id = matchup_record.team_one_id
    #             slot_two_id = matchup_record.team_two_id
    #
    #             if winner_slot_id is not None:
    #                 assert winner_slot_id in (slot_one_id, slot_two_id)
    #
    #             if matchup_record.source_matchup_one_id is not None and slot_one_id is not None:
    #                 source_matchup_one = BracketFactory.get_matchup(bracket_record, matchup_record.source_matchup_one_id)
    #                 assert slot_one_id in (source_matchup_one.slot_one_id, source_matchup_one.slot_two_id)
    #
    #             if matchup_record.source_matchup_two_id is not None and slot_two_id is not None:
    #                 source_matchup_two = BracketFactory.get_matchup(bracket_record, matchup_record.source_matchup_two_id)
    #                 assert slot_two_id in (source_matchup_two.slot_one_id, source_matchup_two.slot_two_id)
