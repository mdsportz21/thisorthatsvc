import os
import urllib.parse
from typing import List

from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

from bracket import record

mongo_host = os.environ.get('MONGO_HOST') or 'localhost'
mongo_port = int(os.environ.get('MONGO_PORT') or 27017)
mongo_db = os.environ.get('MONGO_DB') or 'thisorthat'
mongo_username = os.environ.get('MONGO_USERNAME')
mongo_password = os.environ.get('MONGO_PASSWORD')

client = MongoClient('mongodb://%s:%s@%s:%s/%s' % (
    urllib.parse.quote_plus(mongo_username), urllib.parse.quote_plus(mongo_password), mongo_host,
    mongo_port, mongo_db)) if mongo_username else MongoClient(mongo_host, mongo_port)

db = client[mongo_db]


def store_bracket_field(bracket_field_name: str, teams: List[record.UnseededTeam]) -> None:
    bracket_field = record.BracketField(_id=ObjectId(), name=bracket_field_name, teams=teams)
    db.bracket_fields.find_one_and_replace(filter={'_id': bracket_field.id},
                                           replacement=bracket_field.to_document(),
                                           upsert=True,
                                           return_document=ReturnDocument.AFTER)


def get_all_bracket_fields() -> List[record.BracketField]:
    bracket_field_documents = db.bracket_fields.find()
    return [record.BracketField.from_document(doc) for doc in bracket_field_documents]


def fetch_bracket_field_by_id(bracket_field_id: ObjectId) -> record.BracketField:
    bracket_field_document = db.bracket_fields.find_one({'_id': bracket_field_id})
    return record.BracketField.from_document(bracket_field_document)


def store_bracket_instance(bracket_instance: record.BracketInstance) -> None:
    db.bracket_instances.find_one_and_replace(filter={'_id': bracket_instance.id},
                                              replacement=bracket_instance.to_document(),
                                              upsert=True,
                                              return_document=ReturnDocument.AFTER)


def fetch_bracket_instance(bracket_field_id: ObjectId, bracket_instance_id: ObjectId) -> record.BracketInstance:
    bracket_instance_document = db.bracket_instances.find_one(
        {'_id': bracket_instance_id, 'bracket_field._id': bracket_field_id})
    return record.BracketInstance.from_document(bracket_instance_document)
