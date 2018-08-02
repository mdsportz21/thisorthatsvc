from typing import Dict, Type


class Record(object):
    """
    To be saved in DB.
    """

    def to_document(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def from_document(cls, doc: Dict):
        raise NotImplementedError


class DTO(object):
    """
    'Lite' version of Record, to be sent to front end.
    """

    def to_record(self):
        # type: (DTO) -> Record
        raise NotImplementedError

    @classmethod
    def from_record(cls, record):
        # type: (Type[DTO], Record) -> DTO
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError
