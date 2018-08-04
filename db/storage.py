# from typing import List
#
# from bson import ObjectId
# from flask_pymongo import PyMongo
# from model.record import TeamRecord
# from pymongo import ReturnDocument, UpdateMany, MongoClient
#
# client = MongoClient('localhost', 27017)
# db = client.thisorthat
#
#
# class TeamDAO(object):
#     """
#     :type pymongo: PyMongo
#     """
#
#     def __init__(self, pymongo):
#         self.pymongo = pymongo
#
#     def store_team_records(self, team_records):
#         # type: (list[TeamRecord]) -> (list[TeamRecord])
#         # self.mongo.db.subjects.insert_many(to_dicts(subject_records))
#         updated_team_records = []
#         for team_record in team_records:
#             record_filter = {'name': team_record.name, 'img_link': team_record.img_link,
#                              'grouping': team_record.grouping}
#             record_replacement = {'$set': team_record.to_document()}
#             updated_record = db.teams.find_one_and_update(record_filter, record_replacement,
#                                                           upsert=True,
#                                                           return_document=ReturnDocument.AFTER)
#             team_record.id = updated_record['_id']
#             updated_team_records.append(team_record)
#
#         return updated_team_records
#
#     def get_team_documents(self, _filter=None):
#         # type: () -> list[dict]
#         if _filter is None:
#             _filter = {}
#         return list(db.teams.find(_filter))
#
#     def get_team_document(self, team_id):
#         # type: (ObjectId) -> dict
#         return db.teams.find_one({'_id': team_id})
#
#     def get_team_documents_with_grouping_with_max_count(self):
#         # type: () -> list[dict]
#         pipeline = [
#             {"$match": {"grouping": {"$exists": True, "$ne": "MILB"}}},
#             {"$group": {"_id": "$_grouping", "count": {"$sum": 1}}},
#             {"$sort": {"count": -1}}
#         ]
#
#         groupings = list(db.teams.aggregate(pipeline))
#         if len(groupings) == 0:
#             return []
#
#         grouping = groupings[0]['_id']
#
#         return list(db.teams.find({"grouping": grouping}))
#
#     def store_dupes(self, name, team_ids: List[ObjectId]) -> None:
#         requests = [UpdateMany({"_id": {"$in": team_ids}}, {"$set": {"duplicate": True}}),
#                     UpdateMany({"_id": {"$nin": team_ids}, "grouping": {"$eq": name}},
#                                {"$set": {"duplicate": False}}),
#                     UpdateMany({"grouping": {"$eq": name}}, {"$set": {"grouping": "MILB"}})]
#         db.teams.bulk_write(requests)
#
#     def get_unique_team_records_by_grouping(self, grouping_name):
#         # type: (str) -> list[dict]
#         return self.get_team_documents({'duplicate': False, 'grouping': 'MILB'})
