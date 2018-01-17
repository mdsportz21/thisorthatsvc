from bson import ObjectId
from flask_pymongo import PyMongo
from pymongo import ReturnDocument

from model.record import TeamRecord, BracketRecord, SlotRecord
from util import to_dict


class BracketDAO(object):
    """
    :type mongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_bracket(self, bracket_record):
        # type: (BracketRecord) -> BracketRecord
        updated_record = self.pymongo.db.brackets.find_one_and_replace({'_id': bracket_record.id}, to_dict(bracket_record),
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)
        bracket_record.id = updated_record['_id']
        return bracket_record

    def get_bracket(self, name):
        return self.pymongo.db.brackets.find_one({'_name': name})


class SlotDAO(object):
    """
    :type mongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_slots(self, slot_records):
        # type: (list[SlotRecord]) -> (list[SlotRecord])
        # self.mongo.db.subjects.insert_many(to_dicts(subject_records))
        updated_slot_records = []
        for slot_record in slot_records:
            record_filter = {'_id': slot_record.id}
            record_replacement = {'$set': to_dict(slot_record, True)}
            updated_record = self.pymongo.db.slots.find_one_and_update(record_filter, record_replacement,
                                                                       upsert=True,
                                                                       return_document=ReturnDocument.AFTER)
            slot_record.id = updated_record['_id']
            updated_slot_records.append(slot_record)

        return updated_slot_records

    def get_slots(self, bracket_id):
        # type: (ObjectId) -> list[dict]
        return list(self.pymongo.db.slots.find({'bracket_id': bracket_id}))

    def get_slot(self, slot_id):
        # type: (ObjectId) -> dict
        return self.pymongo.db.slots.find_one({'_id': slot_id})


class TeamDAO(object):
    """
    :type pymongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_team_records(self, team_records):
        # type: (list[TeamRecord]) -> (list[TeamRecord])
        # self.mongo.db.subjects.insert_many(to_dicts(subject_records))
        updated_team_records = []
        for team_record in team_records:
            record_filter = {'_name': team_record.name}
            record_replacement = {'$set': to_dict(team_record, True)}
            updated_record = self.pymongo.db.teams.find_one_and_update(record_filter, record_replacement,
                                                                       upsert=True,
                                                                       return_document=ReturnDocument.AFTER)
            team_record.id = updated_record['_id']
            updated_team_records.append(team_record)

        return updated_team_records

    def get_team_records(self):
        # type: () -> list[dict]
        return list(self.pymongo.db.teams.find())

    def get_team_record(self, team_id):
        # type: (ObjectId) -> dict
        return self.pymongo.db.teams.find_one({'_id': team_id})
