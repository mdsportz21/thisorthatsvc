from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from model.record import SubjectRecord
from util import to_dict


class SubjectDAO(object):
    """
    :type mongo: PyMongo
    """

    def __init__(self, mongo):
        self.mongo = mongo

    def store_subjects(self, subject_records):
        """
        :type subject_records: list of SubjectRecord
        """
        self.mongo.db.subjects.insert_many([to_dict(subject_record) for subject_record in subject_records])

    def get_subjects(self):
        """
        :rtype: list of SubjectRecord
        """
        return list(self.mongo.db.subjects.find())

    def update_next(self, current_id, next_id):
        """
        :type current_id: ObjectId
        :type next_id: ObjectId
        """
        self.mongo.db.subjects.find_one_and_update(
            {'_id': current_id}, {'$set': {SubjectRecord.NEXT_SUBJECT_ID_FIELD: next_id}}
        )

    def clear_next(self, subject_id):
        """
        :type subject_id: ObjectId
        """
        self.mongo.db.subjects.find_one_and_update(
            {'_id': subject_id}, {'$unset': {SubjectRecord.NEXT_SUBJECT_ID_FIELD}}
        )
