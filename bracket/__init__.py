from typing import List

from bson import ObjectId

from bracket import dto
from bracket import generator
from bracket import record
from bracket import storage


def generate_and_store_bracket_instance(bracket_field_id: ObjectId, seeding_strategy: str,
                                        user: str) -> dto.BracketInstance:
    # translate seeding strategy to enum
    seeding_strategy = dto.SeedingStrategy[seeding_strategy.upper()]

    # fetch bracket field from DB
    bracket_field = storage.fetch_bracket_field_by_id(bracket_field_id)

    # generate the bracket from the field teams
    bracket_instance = generator.generate_bracket_instance(bracket_field,
                                                           seeding_strategy,
                                                           user)
    # store bracket instance
    storage.store_bracket_instance(bracket_instance)

    # translate record to DTO and return
    return dto.BracketInstance.from_record(bracket_instance)


def generate_bracket_instance(bracket_field_id: ObjectId, seeding_strategy: str, user: str,
                              bracket_size: int) -> dto.BracketInstance:
    # translate seeding strategy to enum
    seeding_strategy = dto.SeedingStrategy[seeding_strategy.upper()]

    # fetch bracket field from DB
    bracket_field = storage.fetch_bracket_field_by_id(bracket_field_id)

    # generate the bracket from the field teams
    bracket_instance = generator.generate_bracket_instance(bracket_field,
                                                           seeding_strategy,
                                                           user,
                                                           bracket_size)

    # translate record to DTO and return
    return dto.BracketInstance.from_record(bracket_instance)


def get_all_bracket_fields() -> List[dto.BracketField]:
    return [dto.BracketField.from_record(bracket_field_record) for bracket_field_record in
            storage.get_all_bracket_fields()]


def fetch_bracket_instance(bracket_field_id: ObjectId, bracket_instance_id: ObjectId) -> dto.BracketInstance:
    bracket_instance = storage.fetch_bracket_instance(bracket_field_id, bracket_instance_id)
    return dto.BracketInstance.from_record(bracket_instance)


def fetch_bracket_instances(bracket_field_id: ObjectId, user: str) -> List[dto.BracketInstance]:
    bracket_instances = storage.fetch_bracket_instances(bracket_field_id, user)
    return [dto.BracketInstance.from_record(bracket_instance) for bracket_instance in bracket_instances]


def save_bracket_instance(bracket_instance: dto.BracketInstance) -> None:
    # TODO: validate rounds
    record = dto.BracketInstance.to_record(bracket_instance)
    storage.store_bracket_instance(record)
