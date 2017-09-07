from math import log
from random import sample

from model import codec
from model.dto import SubjectDTO
from model.record import Bracket, Round, TeamSlot, Team, Matchup, MatchupSlot


class BracketFactory(object):
    @staticmethod
    def generate_bracket(subjects, name):
        # type: (list[Team]) -> Bracket
        if len(subjects) < 2:
            raise NotEnoughTeamsException(
                'At least 2 teams required to generate a bracket. Found {0} teams.'.format(len(subjects)))
        num_rounds = BracketFactory.get_num_rounds(subjects)
        bracket = Bracket([], name)
        round_one = BracketFactory.create_first_round(subjects)
        bracket.append_round(round_one)
        if num_rounds > 1:
            bracket.append_empty_rounds(num_rounds - 1)
        return bracket

    @staticmethod
    def generate_bracket_from_dtos(subject_dtos, name):
        # type: (list[SubjectDTO]) -> Bracket
        subjects = codec.to_subjects(subject_dtos)
        return BracketFactory.generate_bracket(subjects, name)

    @staticmethod
    def create_first_round(subjects):
        # type: (list[Team]) -> Round
        round_one = Round([])
        randomized_subjects = sample(subjects, len(subjects))
        total_num_teams = len(subjects)
        top_seed = 1
        bottom_seed = total_num_teams
        num_playin_games = total_num_teams % 4 if total_num_teams >= 4 else total_num_teams % 2

        playin_matchup_slots = []
        for i in range(0, num_playin_games):
            team_one = randomized_subjects.pop()
            seed_one = bottom_seed - i
            team_slot_one = TeamSlot(team=team_one, seed=seed_one)

            team_two = randomized_subjects.pop()
            seed_two = bottom_seed - num_playin_games * 2 + i + 1
            team_slot_two = TeamSlot(team=team_two, seed=seed_two)

            matchup = Matchup(slot_one=team_slot_one, slot_two=team_slot_two)
            playin_matchup_slot = MatchupSlot(matchup=matchup)

            playin_matchup_slots.append(playin_matchup_slot)

        bottom_seed -= num_playin_games * 2
        bottom_idx = len(randomized_subjects) - 1

        for i in range(0, len(randomized_subjects)):
            if i > bottom_idx:
                break

            team_one = randomized_subjects[i]
            slot_one = TeamSlot(team_one, top_seed)
            top_seed += 1

            if len(playin_matchup_slots) > 0:
                slot_two = playin_matchup_slots.pop()
            else:
                team_two = randomized_subjects[bottom_idx]
                slot_two = TeamSlot(team_two, bottom_seed)
                bottom_seed -= 1
                bottom_idx -= 1
                pass

            matchup = Matchup(slot_one, slot_two)
            round_one.matchups.append(matchup)

        while playin_matchup_slots:
            slot_one = playin_matchup_slots.pop()
            slot_two = playin_matchup_slots.pop()
            matchup = Matchup(slot_one, slot_two)
            round_one.matchups.append(matchup)

        return round_one

    @staticmethod
    def get_num_rounds(subjects):
        # type: (list[Team]) -> int
        num_teams = len(subjects)
        # Play in games don't count as a round, so don't do ceiling
        # return int(ceil(log(num_teams, 2)))
        return int(log(num_teams, 2))


class NotEnoughTeamsException(Exception):
    pass
