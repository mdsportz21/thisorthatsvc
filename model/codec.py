from bson import ObjectId

from model.dto import SubjectDTO
from model.record import SubjectRecord, Subject


def to_subject(subject_dto):
    """
    :type subject_dto: SubjectDTO
    :rtype: Subject
    """
    subject = Subject(name=subject_dto.name,
                      description=subject_dto.description,
                      img_link=subject_dto.imgLink,
                      level=subject_dto.level,
                      affiliate=subject_dto.affiliate,
                      address=subject_dto.address)
    return subject


def to_subjects(subject_dtos):
    """
    :param subject_dtos: list of SubjectDTO
    :return: list of Subject
    """
    return [to_subject(dto) for dto in subject_dtos]


def to_subject_record(subject_dto):
    """
    :type subject_dto: SubjectDTO
    :rtype: SubjectRecord
    """
    subject_record = SubjectRecord(name=subject_dto.name,
                                   description=subject_dto.description,
                                   img_link=subject_dto.imgLink,
                                   level=subject_dto.level,
                                   affiliate=subject_dto.affiliate,
                                   address=subject_dto.address)
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
    subject_dto = SubjectDTO(name=subject_record.name,
                             imgLink=subject_record.img_link,
                             subjectId=str(subject_record.id) if subject_record.id is not None else None)
    return subject_dto


def from_subject_records(subject_records):
    """
    :param subject_records: list of SubjectRecord
    :return: list of SubjectDTO
    """
    return [from_subject_record(record) for record in subject_records]
