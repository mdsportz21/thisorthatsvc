from typing import Optional, Dict

from bson import ObjectId

import base


class Team(base.Record):
    """ Unseeded.
    :type _id: ObjectId
    :type _name: str
    :type _img_link: str
    """

    def __init__(self, _id: ObjectId, name: str, img_link: str) -> None:
        self._id = _id
        self._name = name
        self._img_link = img_link

    @property
    def id(self) -> ObjectId:
        return self._id

    @id.setter
    def id(self, value: ObjectId) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def img_link(self) -> str:
        return self._img_link

    @img_link.setter
    def img_link(self, value: str) -> None:
        self._img_link = value

    def to_document(self) -> Dict:
        return {
            '_id': self.id,
            'name': self.name,
            'img_link': self.img_link
        }

    @classmethod
    def from_document(cls, doc: Dict) -> 'Team':
        return cls(
            _id=doc['_id'],
            name=doc['name'],
            img_link=doc['img_link']
        )


class Participant(Team):
    """ A tournament participant is a seeded team.
    :type _seed: int
    """

    def __init__(self, _id: ObjectId, name: str, img_link: str, seed: int) -> None:
        Team.__init__(self, _id, name, img_link)
        self._seed = seed

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        self._seed = value

    def to_document(self) -> Dict:
        doc = super().to_document()
        doc['seed'] = self.seed
        return doc

    @classmethod
    def from_document(cls, doc: Dict) -> 'Participant':
        return cls(
            _id=doc['_id'],
            name=doc['name'],
            img_link=doc['img_link'],
            seed=doc['seed']
        )


class Matchup(base.Record):
    """
    :type _id: ObjectId
    :type _team_one: Participant
    :type _team_two: Participant
    :type _source_matchup_one: Matchup
    :type _source_matchup_two: Matchup
    :type _winner_team_id: ObjectId
    """

    def __init__(self,
                 _id: ObjectId,
                 team_one: Optional[Participant],
                 team_two: Optional[Participant],
                 source_matchup_one: 'Optional[Matchup]',
                 source_matchup_two: 'Optional[Matchup]',
                 winner_team_id: Optional[ObjectId]) -> None:
        self._id = _id
        self._team_one = team_one
        self._team_two = team_two
        self._source_matchup_one = source_matchup_one
        self._source_matchup_two = source_matchup_two
        self._winner_team_id = winner_team_id

    @property
    def id(self) -> ObjectId:
        return self._id

    @id.setter
    def id(self, value: ObjectId) -> None:
        self._id = value

    @property
    def team_one(self) -> Participant:
        return self._team_one

    @team_one.setter
    def team_one(self, value: Participant) -> None:
        self._team_one = value

    @property
    def team_two(self) -> Participant:
        return self._team_two

    @team_two.setter
    def team_two(self, value: Participant) -> None:
        self._team_two = value

    @property
    def source_matchup_one(self) -> 'Matchup':
        return self._source_matchup_one

    @source_matchup_one.setter
    def source_matchup_one(self, value: 'Matchup') -> None:
        self._source_matchup_one = value

    @property
    def source_matchup_two(self) -> 'Matchup':
        return self._source_matchup_two

    @source_matchup_two.setter
    def source_matchup_two(self, value: 'Matchup') -> None:
        self._source_matchup_two = value

    @property
    def winner_team_id(self) -> ObjectId:
        return self._winner_team_id

    @winner_team_id.setter
    def winner_team_id(self, value: ObjectId) -> None:
        self._winner_team_id = value

    def to_document(self) -> Dict:
        return {
            '_id': self.id,
            'team_one': self.team_one.to_document(),
            'team_two': self.team_two.to_document(),
            'source_matchup_one': self.source_matchup_one.to_document(),
            'source_matchup_two': self.source_matchup_two.to_document(),
            'winner_team_id': self.winner_team_id
        }

    @classmethod
    def from_document(cls, doc: Dict) -> 'Matchup':
        return cls(
            _id=doc['_id'],
            team_one=Participant.from_document(doc['team_one']),
            team_two=Participant.from_document(doc['team_two']),
            source_matchup_one=Matchup.from_document(doc['source_matchup_one']),
            source_matchup_two=Matchup.from_document(doc['source_matchup_two']),
            winner_team_id=doc['winner_team_id']
        )

#
# class Round(base.Record):
#     """ Round of a bracket instance
#     :type matchups: list of Matchup
#     """
#
#     def __init__(self, matchups: List[Matchup]) -> None:
#         self._matchups = matchups
#
#     @property
#     def matchups(self):
#         return self._matchups
#
#     @matchups.setter
#     def matchups(self, value):
#         self._matchups = value
#
#     def to_document(self) -> Dict:
#         return dict(
#             matchups=[matchup.to_document() for matchup in self.matchups]
#         )
#
#     @classmethod
#     def from_document(cls, doc) -> 'Round':
#         return cls(
#             matchups=[Matchup.from_document(matchup_document) for matchup_document in
#                       doc['matchups']]
#         )
#
#
#
# class BracketField(base.Record):
#     """ the set of unique elements to be seeded in bracket instances
#     :type _id: ObjectId
#     :type _name: str
#     :type _teams: list of UnseededTeam
#     """
#
#     def __init__(self, _id: ObjectId, name: str, teams: List[UnseededTeam]) -> None:
#         self._id = _id
#         self._name = name
#         self._teams = teams
#
#     @property
#     def id(self):
#         return self._id
#
#     @id.setter
#     def id(self, value):
#         self._id = value
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, value):
#         self._name = value
#
#     @property
#     def teams(self):
#         return self._teams
#
#     @teams.setter
#     def teams(self, value):
#         self._teams = value
#
#     def to_document(self) -> Dict:
#         return dict(
#             _id=self.id,
#             name=self.name,
#             teams=[team.to_document() for team in self.teams]
#         )
#
#     @classmethod
#     def from_document(cls, doc: dict) -> 'BracketField':
#         return cls(
#             _id=doc['_id'],
#             name=doc['name'],
#             teams=[UnseededTeam.from_document(team_document) for team_document in doc['teams']]
#         )
#
#
# class BracketInstance(base.Record):
#     """ a user’s attempt at filling out a bracket
#     :type _id: ObjectId
#     :type _rounds: list of Round
#     :type _user: str
#     :type _bracket_field: BracketField
#     :type _created_on: datetime
#     :type _updated_on: datetime
#     """
#
#     def __init__(self, _id: ObjectId, rounds: List[Round], user: str, bracket_field: Optional[BracketField],
#                  created_on: datetime, updated_on: datetime) -> None:
#         self._id = _id
#         self._rounds = rounds
#         self._user = user
#         self._bracket_field = bracket_field
#         self._created_on = created_on
#         self._updated_on = updated_on
#
#     @property
#     def id(self):
#         return self._id
#
#     @id.setter
#     def id(self, value):
#         self._id = value
#
#     @property
#     def rounds(self):
#         return self._rounds
#
#     @rounds.setter
#     def rounds(self, value):
#         self._rounds = value
#
#     @property
#     def user(self):
#         return self._user
#
#     @user.setter
#     def user(self, value):
#         self._user = value
#
#     @property
#     def bracket_field(self):
#         return self._bracket_field
#
#     @bracket_field.setter
#     def bracket_field(self, value):
#         self._bracket_field = value
#
#     @property
#     def created_on(self):
#         return self._created_on
#
#     @created_on.setter
#     def created_on(self, value):
#         self._created_on = value
#
#     @property
#     def updated_on(self):
#         return self._updated_on
#
#     @updated_on.setter
#     def updated_on(self, value):
#         self._updated_on = value
#
#     def to_document(self) -> Dict:
#         return dict(
#             _id=self.id,
#             rounds=[round.to_document() for round in self.rounds],
#             user=self.user,
#             bracket_field=self.bracket_field.to_document(),
#             created_on=self.created_on,
#             updated_on=self.updated_on
#         )
#
#     @classmethod
#     def from_document(cls, doc: dict) -> 'BracketInstance':
#         return cls(
#             _id=doc['_id'],
#             rounds=[Round.from_document(round_document) for round_document in doc['rounds']],
#             user=doc['user'],
#             bracket_field=BracketField.from_document(doc['bracket_field']),
#             created_on=doc['created_on'],
#             updated_on=doc['updated_on']
#         )
