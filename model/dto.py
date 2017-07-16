from bson.objectid import ObjectId
import six


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
