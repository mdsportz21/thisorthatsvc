import collections
from decimal import Decimal


def to_dict(obj):
    """
    Recursively convert a Python object graph to sequences (lists)
    and mappings (dicts) of primitives (bool, int, float, string, ...)
    """
    if isinstance(obj, basestring):
        return obj
    elif isinstance(obj, dict):
        return dict((key, to_dict(val)) for key, val in obj.items())
    elif isinstance(obj, collections.Iterable):
        return [to_dict(val) for val in obj]
    elif hasattr(obj, '__dict__'):
        return to_dict(vars(obj))
    elif hasattr(obj, '__slots__'):
        return to_dict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
    return obj


def to_dicts(objs):
    """
    :param objs: list of object
    :return: list of dict
    """
    return [to_dict(obj) for obj in objs]


def divide(a, b, precision=4):
    """
    :type a: float
    :type b: float
    :type precision: int
    :rtype: float
    """
    return float(Decimal(a / Decimal(b)).quantize(Decimal('1e-' + str(precision))))
