from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from model.record import SubjectRecord
from util import to_dicts
from model.record import Victim


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
        self.mongo.db.subjects.insert_many(to_dicts(subject_records))

    def get_subjects(self):
        """
        :rtype: list
        """
        return list(self.mongo.db.subjects.find())

    def get_subject(self, subject_id):
        """
        :param subject_id: ObjectId
        :rtype:
        """
        return self.mongo.db.subjects.find_one({'_id': subject_id})

    def update_victims(self, subject_id, victims):
        """
        :type subject_id: ObjectId
        :type victims: set of Victim
        """
        self.mongo.db.subjects.find_one_and_update(
            {'_id': subject_id}, {'$set': {'_victims': list(to_dicts(victims))}}
        )
