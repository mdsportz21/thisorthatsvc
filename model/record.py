from arrow import Arrow
from bson.objectid import ObjectId


class Victim(object):
    """
    :type victim_id: ObjectId
    :type battle_date:
    """

    def __init__(self, victim_id=None, battle_date=None):
        self._victim_id = victim_id
        self._battle_date = battle_date

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

    @staticmethod
    def create_victim(victim_id):
        return Victim(victim_id, Arrow.utcnow())


class SubjectRecord(object):
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
        return subject

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

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
