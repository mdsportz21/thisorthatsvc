from model.dto import SubjectDTO
from model.record import SubjectRecord
from bson import ObjectId


def to_subject_record(subject_dto):
    """
    :type subject_dto: SubjectDTO
    :rtype: SubjectRecord
    """
    subject_record = SubjectRecord(img_desc=subject_dto.imgDesc,
                                   description=subject_dto.description,
                                   img_link=subject_dto.imgLink)
    subject_record.id = ObjectId(subject_dto.subjectId) if subject_dto.subjectId is not None else None
    return subject_record


def to_subject_records(subject_dtos):
    """
    :param subject_dtos: list of SubjectDTO
    :return: list of SubjectRecord
    """
    return [to_subject_record(dto) for dto in subject_dtos]


def from_subject_record(subject_record):
    """
    :type subject_record: SubjectRecord
    :rtype: SubjectDTO
    """
    subject_dto = SubjectDTO(imgDesc=subject_record.img_desc,
                             description=subject_record.description,
                             imgLink=subject_record.img_link)
    subject_dto.subjectId = str(subject_record.id) if subject_record.id is not None else None
    return subject_dto


def from_subject_records(subject_records):
    """
    :param subject_records: list of SubjectRecord
    :return: list of SubjectDTO
    """
    return [from_subject_record(record) for record in subject_records]
