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

    def udpate_victims(self, subject_id, victims):
        """
        :type subject_id: ObjectId
        :type victims: set
        """
        self.mongo.db.subjects.find_one_and_update(
            {'_id': subject_id}, {'$set': {'_victims': victims}}
        )
