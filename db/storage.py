from flask_pymongo import PyMongo
from pymongo import ReplaceOne

from model.record import SubjectRecord, Bracket
from util import to_dict, to_dicts


class BracketDAO(object):
    """
    :type mongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_bracket(self, bracket):
        """
        :type bracket: Bracket
        """
        bracket_dict = to_dict(bracket)
        self.pymongo.db.brackets.insert_one(bracket_dict)


class SubjectDAO(object):
    """
    :type pymongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_subjects(self, subject_records):
        """
        :type subject_records: list of SubjectRecord
        """
        # self.mongo.db.subjects.insert_many(to_dicts(subject_records))
        requests = []
        for subject_record in subject_records:
            record_filter = {'_description': subject_record.description}
            record_replacement = to_dict(subject_record)
            replace_one = ReplaceOne(record_filter, record_replacement, True)
            requests.append(replace_one)
        result = self.pymongo.db.subjects.bulk_write(requests)
        return result

    def get_subjects(self):
        """
        :rtype: list
        """
        return list(self.pymongo.db.subjects.find())

    def get_subject(self, subject_id):
        """
        :param subject_id: ObjectId
        :rtype:
        """
        return self.pymongo.db.subjects.find_one({'_id': subject_id})

    def update_victims(self, subject_record):
        # type: (SubjectRecord) -> None
        self.pymongo.db.subjects.find_one_and_update(
            {'_id': subject_record.id}, {'$set': {'_victims': list(to_dicts(subject_record.victims))}}
        )
