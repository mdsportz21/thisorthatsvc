from bson import ObjectId
from flask_pymongo import PyMongo
from pymongo import ReturnDocument, UpdateMany

from model.record import TeamRecord, BracketRecord
from util import to_dict
from typing import List



class BracketDAO(object):
    """
    :type mongo: PyMongo
    """

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def store_bracket(self, bracket_record):
        # type: (BracketRecord) -> BracketRecord
        updated_record = self.pymongo.db.brackets.find_one_and_replace({'_id': bracket_record.id},
                                                                       to_dict(bracket_record),
                                                                       upsert=True,
                                                                       return_document=ReturnDocument.AFTER)
        bracket_record.id = updated_record['_id']
        return bracket_record

    def get_bracket(self, name):
        return self.pymongo.db.brackets.find_one({'_name': name})


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
            record_filter = {'_name': team_record.name, '_img_link': team_record.img_link,
                             '_grouping': team_record.grouping}
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

    def get_teams_with_grouping_with_max_count(self):
        pipeline = [
            {"$match": {"_grouping": {"$exists": True, "$ne": "MILB"}}},
            {"$group": {"_id": "$_grouping", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]

        groupings = list(self.pymongo.db.teams.aggregate(pipeline))
        if len(groupings) == 0:
            return []

        grouping = groupings[0]['_id']

        return list(self.pymongo.db.teams.find({"_grouping": grouping}))

    def store_dupes(self, name, team_ids: List[ObjectId]) -> None:
        requests = [UpdateMany({"_id": {"$in": team_ids}}, {"$set": {"_duplicate": True}}),
                    UpdateMany({"_id": {"$nin": team_ids}, "_grouping": {"$eq": name}}, {"$set": {"_duplicate": False}}),
                    UpdateMany({"_grouping": {"$eq": name}}, {"$set": {"_grouping": "MILB"}})]
        self.pymongo.db.teams.bulk_write(requests)
