import unittest

from bracket import BracketFactory
from bracket import NotEnoughTeamsException
from model.dto import SubjectDTO
from model.record import MatchupSlot, TeamSlot, Bracket
from util import to_dict


class BracketFactoryTest(unittest.TestCase):
    def test_generate_bracket_no_teams_throws_exception(self):
        dtos = []
        with self.assertRaises(NotEnoughTeamsException):
            BracketFactory.generate_bracket_from_dtos(dtos, '')

    def test_generate_bracket_one_team_throws_exception(self):
        dtos = [SubjectDTO()]
        with self.assertRaises(NotEnoughTeamsException):
            BracketFactory.generate_bracket_from_dtos(dtos, '')

    def test_generate_bracket_five_teams(self):
        dtos = []
        for i in range(0, 5):
            dtos.append(SubjectDTO())

        bracket = BracketFactory.generate_bracket_from_dtos(dtos, '')

        self.assertIsNotNone(bracket)

        rounds = bracket.rounds
        self.assertEqual(len(rounds), 2)

        round_one = rounds[0]
        matchups = round_one.matchups
        self.assertEqual(len(matchups), 2)

        playin_matchup = round_one.get_matchup_by_seed(5)
        self.assertIsNotNone(playin_matchup)
        sorted_playin_slots = get_sorted_slots(playin_matchup)
        self.assertEqual(sorted_playin_slots[0].seed, 4)
        self.assertEqual(sorted_playin_slots[1].seed, 5)

        one_matchup = round_one.get_matchup_by_seed(1)
        playin_matchup_slots = one_matchup.get_slots_by_type(MatchupSlot)
        self.assertEqual(playin_matchup, playin_matchup_slots[0].matchup)

        one_team_slots = one_matchup.get_slots_by_type(TeamSlot)
        self.assertEqual(one_team_slots[0].seed, 1)

        two_three_matchup = round_one.get_matchup_by_seed(2)
        two_three_slots_sorted = get_sorted_slots(two_three_matchup)
        self.assertEqual(two_three_slots_sorted[0].seed, 2)
        self.assertEqual(two_three_slots_sorted[1].seed, 3)

    def test_generate_bracket_seven_teams(self):
        dtos = []
        for i in range(0, 7):
            dtos.append(SubjectDTO())

        bracket = BracketFactory.generate_bracket_from_dtos(dtos, '')

        self.assertIsNotNone(bracket)

        rounds = bracket.rounds
        self.assertEqual(len(rounds), 2)

        round_one = rounds[0]
        matchups = round_one.matchups
        self.assertEqual(len(matchups), 2)

        playin_matchup = round_one.get_matchup_by_seed(5)
        self.assertIsNotNone(playin_matchup)
        sorted_playin_slots = get_sorted_slots(playin_matchup)
        self.assertEqual(sorted_playin_slots[0].seed, 4)
        self.assertEqual(sorted_playin_slots[1].seed, 5)

        one_matchup = round_one.get_matchup_by_seed(1)
        playin_matchup_slots = one_matchup.get_slots_by_type(MatchupSlot)
        self.assertEqual(playin_matchup, playin_matchup_slots[0].matchup)

        one_team_slots = one_matchup.get_slots_by_type(TeamSlot)
        self.assertEqual(one_team_slots[0].seed, 1)

        two_seven_matchup = round_one.get_matchup_by_seed(2)
        two_seven_slots_sorted = get_sorted_slots(two_seven_matchup)
        self.assertEqual(two_seven_slots_sorted[0].seed, 2)
        self.assertEqual(two_seven_slots_sorted[1].seed, 7)

    def test_generate_bracket_two_teams(self):
        dtos = [SubjectDTO(), SubjectDTO()]
        bracket = BracketFactory.generate_bracket_from_dtos(dtos, '')
        self.assertIsNotNone(bracket)
        rounds = bracket.rounds
        self.assertEqual(len(rounds), 1)
        matchups = rounds[0].matchups
        self.assertEqual(len(matchups), 1)
        matchup = matchups[0]

        self.assertIsInstance(matchup.slot_one, TeamSlot)
        self.assertIsNotNone(matchup.slot_one.team)
        self.assertIsNotNone(matchup.slot_one.seed)

        self.assertIsInstance(matchup.slot_two, TeamSlot)
        self.assertIsNotNone(matchup.slot_two.team)
        self.assertIsNotNone(matchup.slot_two.seed)

        slots = get_sorted_slots(matchup)
        self.assertEqual(slots[0].seed, 1)
        self.assertEqual(slots[1].seed, 2)

    def test_generate_bracket_todict(self):
        dtos = [SubjectDTO(), SubjectDTO()]
        original_bracket = BracketFactory.generate_bracket_from_dtos(dtos, 'test bracket')
        bracket_dict = to_dict(original_bracket)
        new_bracket = Bracket.factory(bracket_dict)
        self.assertEqual(original_bracket, new_bracket)


def get_sorted_slots(matchup):
    slots = [matchup.slot_one, matchup.slot_two]
    slots = sorted(slots, key=slot_sort_fn)
    return slots


def slot_sort_fn(slot):
    return slot.seed


if __name__ == '__main__':
    unittest.main()
