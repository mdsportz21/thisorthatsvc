from typing import Optional, Dict
from datetime import datetime

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
    :type _team_one: Participant
    :type _team_two: Participant
    :type _source_matchup_one: Matchup
    :type _source_matchup_two: Matchup
    """

    def __init__(self,
                 team_one: Optional[Participant],
                 team_two: Optional[Participant],
                 source_matchup_one: 'Optional[Matchup]',
                 source_matchup_two: 'Optional[Matchup]') -> None:
        self._team_one = team_one
        self._team_two = team_two
        self._source_matchup_one = source_matchup_one
        self._source_matchup_two = source_matchup_two

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

    def to_document(self) -> Dict:
        return {
            'team_one': self.team_one.to_document(),
            'team_two': self.team_two.to_document(),
            'source_matchup_one': self.source_matchup_one.to_document(),
            'source_matchup_two': self.source_matchup_two.to_document()
        }

    @classmethod
    def from_document(cls, doc: Dict) -> 'Matchup':
        return cls(
            team_one=Participant.from_document(doc['team_one']),
            team_two=Participant.from_document(doc['team_two']),
            source_matchup_one=Matchup.from_document(doc['source_matchup_one']),
            source_matchup_two=Matchup.from_document(doc['source_matchup_two'])
        )


class Bracket(base.Record):
    """
    :type _id: ObjectId
    :type final: Matchup
    :type user_id: ObjectId
    :type created_at: datetime
    :type last_updated_at: datetime
    :type field_hash: int
    :type seeding_hash: int
    """

    def __init__(self, _id: ObjectId, final: Matchup, user_id: ObjectId, created_at: datetime,
                 last_updated_at: datetime, field_hash: int, seeding_hash: int) -> None:
        self._id = _id
        self._final = final
        self._user_id = user_id
        self._created_at = created_at
        self._last_updated_at = last_updated_at
        self._field_hash = field_hash
        self._seeding_hash = seeding_hash

    @property
    def id(self) -> ObjectId:
        return self._id

    @id.setter
    def id(self, value: ObjectId) -> None:
        self._id = value

    @property
    def final(self) -> Matchup:
        return self._final

    @final.setter
    def final(self, value: Matchup) -> None:
        self._final = value

    @property
    def user_id(self) -> ObjectId:
        return self._user_id

    @user_id.setter
    def user_id(self, value: ObjectId) -> None:
        self._user_id = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime) -> None:
        self._created_at = value

    @property
    def last_updated_at(self) -> datetime:
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, value: datetime) -> None:
        self._last_updated_at = value

    @property
    def field_hash(self) -> int:
        return self._field_hash

    @field_hash.setter
    def field_hash(self, value: int) -> None:
        self._field_hash = value

    @property
    def seeding_hash(self) -> int:
        return self._seeding_hash

    @seeding_hash.setter
    def seeding_hash(self, value: int) -> None:
        self._seeding_hash = value

