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
    bracket_instance = generator.generate_bracket_instance(bracket_field.teams,
                                                           seeding_strategy,
                                                           bracket_field.id,
                                                           user)
    # store bracket instance
    storage.store_bracket_instance(bracket_instance)

    # translate record to DTO and return
    return dto.BracketInstance.from_record(bracket_instance)
