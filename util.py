from decimal import Decimal

import jsonpickle
from flask import jsonify

ID_ATTR = '_id'

# def to_dict(obj, delete_id=False):
#     """
#     Recursively convert a Python object graph to sequences (lists)
#     and mappings (dicts) of primitives (bool, int, float, string, ...).
#     Delete *top level* _id field if delete_id is True.
#     """
#     if isinstance(obj, str):
#         return obj
#     elif isinstance(obj, dict):
#         return dict((key, to_dict(val)) for key, val in obj.items() if not delete_id or key != ID_ATTR)
#     elif isinstance(obj, collections.Iterable):
#         return [to_dict(val) for val in obj]
#     elif hasattr(obj, '__dict__'):
#         obj_dict = vars(obj)
#         if delete_id and ID_ATTR in obj_dict:
#             del obj_dict[ID_ATTR]
#         return to_dict(obj_dict)
#     elif isinstance(obj, ObjectId):
#         return obj
#     elif hasattr(obj, '__slots__'):
#         return to_dict(to_dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
#     return obj


# def to_dicts(objs):
#     """
#     :param objs: list of object
#     :return: list of dict
#     """
#     return [to_dict(obj) for obj in objs]


def divide(a, b, precision=4):
    """
    :type a: float
    :type b: float
    :type precision: int
    :rtype: float
    """
    return float(Decimal(a / Decimal(b)).quantize(Decimal('1e-' + str(precision))))


def to_json(dto):
    # type: (object) -> str
    return jsonpickle.encode(dto, unpicklable=False)
