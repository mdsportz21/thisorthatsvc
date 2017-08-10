import arrow
import six
from bson.objectid import ObjectId


class BaseRecord(object):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class Victim(BaseRecord):
    """
    :type victim_id: ObjectId
    :type battle_date: arrow.Arrow
    :type explicit: bool
    """

    def __init__(self, victim_id=None, battle_date=None, explicit=None):
        self._victim_id = victim_id
        self._battle_date = battle_date
        self._explicit = explicit

    def __eq__(self, other):
        return self.victim_id == other.victim_id

    def __hash__(self):
        return hash(self.victim_id)

    def __str__(self):
        return str(self.victim_id) + ': ' + str(self._battle_date)

    @property
    def victim_id(self):
        return self._victim_id

    @victim_id.setter
    def victim_id(self, value):
        self._victim_id = value

    @property
    def battle_date(self):
        return self._battle_date

    @battle_date.setter
    def battle_date(self, value):
        self._battle_date = value

    @property
    def explicit(self):
        return self._explicit

    @explicit.setter
    def explicit(self, value):
        self._explicit = value

    @staticmethod
    def create_victim(victim_id, is_explicit=True):
        # type: (ObjectId, bool) -> Victim
        return Victim(victim_id, arrow.Arrow.utcnow(), is_explicit)

    @staticmethod
    def victim_factory(victim_dict):
        """
        :type victim_dict: dict
        :rtype: Victim
        """
        victim = Victim()
        victim.update(**victim_dict)
        if victim.battle_date is not None and isinstance(victim.battle_date, six.string_types):
            victim.battle_date = arrow.get(victim.battle_date)
        return victim


class SubjectRecord(BaseRecord):
    """
    :type _id: ObjectId
    :type img_desc: str
    :type description: str
    :type img_link: str
    :type victims: set of Victim
    """

    def __init__(self, _id=None, img_desc=None, description=None, img_link=None, victims=None):
        self._id = _id
        self._img_desc = img_desc
        self._description = description
        self._img_link = img_link
        self._victims = victims if victims is not None else set()

    def __eq__(self, other):
        return self._id == other.id

    def __hash__(self):
        return hash(self._id)

    @staticmethod
    def subject_record_factory(subject_record_dict):
        """
        :param subject_record_dict: dict
        :return: SubjectRecord
        """
        subject = SubjectRecord()
        subject.update(**subject_record_dict)
        victims = set()
        for victim_dict in subject.victims:
            victims.add(Victim.victim_factory(victim_dict))
        subject.victims = victims
        return subject

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def img_desc(self):
        return self._img_desc

    @img_desc.setter
    def img_desc(self, value):
        self._img_desc = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, value):
        self._img_link = value

    @property
    def victims(self):
        return self._victims

    @victims.setter
    def victims(self, value):
        self._victims = value

    def has_victim(self, subject_id):
        # type: (ObjectId) -> bool
        for victim in self.victims:
            if victim.victim_id == subject_id:
                return True
        return False

    def as_victim(self):
        return Victim.create_victim(self.id)
