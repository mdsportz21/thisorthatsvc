from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from pymongo import ReplaceOne

from model.record import SubjectRecord
from model.record import Victim
import util


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
        # self.mongo.db.subjects.insert_many(to_dicts(subject_records))
        requests = []
        for subject_record in subject_records:
            record_filter = {'_description': subject_record.description}
            record_replacement = util.to_dict(subject_record)
            replace_one = ReplaceOne(record_filter, record_replacement, True)
            requests.append(replace_one)
        result = self.mongo.db.subjects.bulk_write(requests)
        return result

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
            {'_id': subject_id}, {'$set': {'_victims': list(util.to_dicts(victims))}}
        )
