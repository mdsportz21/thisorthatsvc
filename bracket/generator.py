import math
import random
from datetime import datetime
from typing import List, Tuple

from bson import ObjectId

from bracket import record
from bracket.dto import SeedingStrategy
from bracket.record import BracketField


def generate_bracket_instance(bracket_field: BracketField, seeding_strategy: SeedingStrategy,
                              user: str, bracket_size: int = None) -> record.BracketInstance:
    # order the field according to the seeding strategy
    unseeded_teams = list(bracket_field.teams)
    if bracket_size is not None:
        unseeded_teams = unseeded_teams[0:bracket_size]
    if seeding_strategy == SeedingStrategy.RANDOM:
        random.shuffle(unseeded_teams)
    elif seeding_strategy == SeedingStrategy.USER:
        # TODO: order by highest avg finish
        pass

    # assign the seeds
    seeded_teams = [record.SeededTeam(unseeded_team.id, unseeded_team.name, unseeded_team.img_link, i + 1) for
                    i, unseeded_team in enumerate(unseeded_teams)]

    bracket_field.teams = seeded_teams

    # generate the bracket
    rounds = generate_rounds(tuple(seeded_teams))

    return record.BracketInstance(_id=ObjectId(), rounds=rounds, user=user, bracket_field=bracket_field,
                                  created_on=datetime.utcnow(), updated_on=datetime.utcnow())


def get_num_play_in_games(num_teams: int) -> int:
    # examples:
    #   int(7 - 2^floor(log(7,2))) = int(7 - 2^2) = 3
    #   int(9 - 2^floor(log(9,2))) = int(9 - 2^3) = 1
    return int(num_teams - pow(2, math.floor(math.log(num_teams, 2))))


def get_last_team_bye_index(num_teams: int, num_play_in_games: int) -> int:
    return num_teams - num_play_in_games * 2


def generate_play_in_round(teams_final: Tuple[record.SeededTeam], num_play_in_games: int) -> record.Round:
    matchups: List[record.Matchup] = []
    teams = list(teams_final)

    # the play-in round should only have the last num_play_in_games * 2 teams in it
    play_in_index = get_last_team_bye_index(len(teams), num_play_in_games)

    # match the team at play_in_index against the last seeded team remaining
    while play_in_index < len(teams) - 1:
        team_one = teams.pop(play_in_index)
        team_two = teams.pop()
        matchup = record.Matchup(
            _id=ObjectId(),
            team_one_id=team_one.id,
            team_two_id=team_two.id,
            source_matchup_one_id=None,
            source_matchup_two_id=None,
            winner_team_id=None
        )
        matchups.append(matchup)
        # since we're popping records, we don't need to increment the index

    assert len(matchups) == num_play_in_games

    return record.Round(matchups)


def get_middle_seed_index(unassigned_teams: List[record.SeededTeam],
                          play_in_matchups: List[record.Matchup]) -> int:
    # used to determine whether middle matchup comes from unassigned teams or play-in matchups
    return int(math.floor((len(unassigned_teams) + len(play_in_matchups)) / 2))


def generate_first_round(unassigned_teams_final: Tuple[record.SeededTeam],
                         play_in_matchups_final: Tuple[record.Matchup]) -> record.Round:
    unassigned_teams = list(unassigned_teams_final)
    play_in_matchups = list(play_in_matchups_final)

    # teams in first round + play-in games = power of 2
    assert (len(unassigned_teams) + len(play_in_matchups)) % 2 == 0

    matchups: List[record.Matchup] = []

    while unassigned_teams or play_in_matchups:
        team_one_id = None
        team_two_id = None
        source_matchup_one_id = None
        source_matchup_two_id = None

        if matchups:
            # build round from middle out
            middle_seed_index = get_middle_seed_index(unassigned_teams,
                                                      play_in_matchups)
            if middle_seed_index < len(unassigned_teams):
                # the top seed comes from teams
                team_index = middle_seed_index
                team_one_id = unassigned_teams.pop(team_index).id
            else:
                matchup_index = middle_seed_index - len(unassigned_teams)
                source_matchup_one_id = play_in_matchups.pop(matchup_index).id

            # recalculate, since we popped
            middle_seed_index = get_middle_seed_index(unassigned_teams,
                                                      play_in_matchups)
            if middle_seed_index < len(unassigned_teams):
                team_index = middle_seed_index
                team_two_id = unassigned_teams.pop(team_index).id
            else:
                matchup_index = middle_seed_index - len(unassigned_teams)
                source_matchup_two_id = play_in_matchups.pop(matchup_index).id

        else:
            # build round from outside in
            if unassigned_teams:
                team_one_id = unassigned_teams.pop(0).id
            else:
                source_matchup_one_id = play_in_matchups.pop(0).id

            if play_in_matchups:
                source_matchup_two_id = play_in_matchups.pop().id
            else:
                team_two_id = unassigned_teams.pop().id

        matchup = record.Matchup(
            _id=ObjectId(),
            team_one_id=team_one_id,
            team_two_id=team_two_id,
            source_matchup_one_id=source_matchup_one_id,
            source_matchup_two_id=source_matchup_two_id,
            winner_team_id=None
        )
        matchups.append(matchup)

    round = validate_non_play_in_round(matchups)
    return round


def validate_non_play_in_round(matchups: List[record.Matchup]) -> record.Round:
    # number of matchups in each non-play-in round should be a power of 2
    assert math.log(len(matchups), 2) % 1 == 0
    return record.Round(matchups)


def create_next_round(prev_round_matchups: Tuple[record.Matchup]) -> record.Round:
    prev_round_matchup_iter = iter(prev_round_matchups)
    matchups = []
    for prev_round_matchup_one in prev_round_matchup_iter:
        prev_round_matchup_two = next(prev_round_matchup_iter)
        matchup = record.Matchup(
            _id=ObjectId(),
            source_matchup_one_id=prev_round_matchup_one.id,
            source_matchup_two_id=prev_round_matchup_two.id,
            team_one_id=None,
            team_two_id=None,
            winner_team_id=None
        )
        matchups.append(matchup)

    round = validate_non_play_in_round(matchups)
    return round


def generate_rounds(teams_final: Tuple[record.SeededTeam]) -> List[record.Round]:
    rounds: List[record.Round] = []
    # the teams that haven't been assigned to a round
    unassigned_teams = list(teams_final)

    # add seeds to teams
    for i, team in enumerate(unassigned_teams):
        team.seed = i + 1

    # create play-in round
    matchups: List[record.Matchup] = []
    num_teams = len(unassigned_teams)
    num_play_in_games = get_num_play_in_games(num_teams)

    if num_play_in_games > 0:
        play_in_round = generate_play_in_round(tuple(unassigned_teams), num_play_in_games)
        rounds.append(play_in_round)
        play_in_matchups = tuple(play_in_round.matchups)
    else:
        play_in_matchups: Tuple[record.Matchup] = tuple()

    # the play-in teams are in the play-in round, so we can remove them from the teams list
    last_team_bye_index = get_last_team_bye_index(num_teams, num_play_in_games)
    unassigned_teams = unassigned_teams[:last_team_bye_index]

    first_round = generate_first_round(tuple(unassigned_teams), play_in_matchups)
    rounds.append(first_round)

    while len(rounds[-1].matchups) > 1:
        latest_round = create_next_round(tuple(rounds[-1].matchups))
        rounds.append(latest_round)

    return rounds
