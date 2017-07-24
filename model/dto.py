import six
from bson.objectid import ObjectId

from model.record import SubjectRecord


class SubjectDTO(object):
    """
    :type subjectId: ObjectId
    :type imgDesc: str
    :type description: str
    :type imgLink: str
    :type selected: bool
    """

    def __init__(self, subjectId=None, imgDesc=None, description=None, imgLink=None, selected=None):
        self.subjectId = subjectId
        self.imgDesc = imgDesc
        self.description = description
        self.imgLink = imgLink
        self.selected = selected

    @staticmethod
    def subject_dto_factory(subject_dto_dict):
        subject = SubjectDTO()
        subject.update(**subject_dto_dict)
        if subject.subjectId is not None and isinstance(subject.subjectId, six.string_types):
            subject.subjectId = ObjectId(subject.subjectId)
        return subject

    def update(self, **kwargs):
        self.__dict__.update(kwargs)


class RankingDTO(object):
    """
    :type subjectId: ObjectId
    :type imgDesc: str
    :type description: str
    :type imgLink: str
    :type rank: int
    :type victims: list of ObjectId
    :type wins: int
    :type faced: int
    """

    def __init__(self, subject_id=None, img_desc=None, description=None, img_link=None, rank=None, victims=None, wins=0,
                 faced=0):
        self.subjectId = subject_id
        self.imgDesc = img_desc
        self.description = description
        self.imgLink = img_link
        self.rank = rank
        self.victims = victims
        self.wins = wins
        self.faced = faced

    @staticmethod
    def to_ranking_dto(subject_record, rank):
        """
        :type subject_record: SubjectRecord
        :type rank: int
        :rtype: RankingDTO
        """
        victims = [str(victim.victim_id) for victim in subject_record.victims]
        ranking_dto = RankingDTO(subject_id=str(subject_record.id), img_desc=subject_record.img_desc,
                                 description=subject_record.description,
                                 img_link=subject_record.img_link, rank=rank,
                                 victims=victims)
        return ranking_dto
