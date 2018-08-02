from typing import List

from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

from bracket import record

client = MongoClient('localhost', 27017)
db = client.thisorthat


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