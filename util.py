from decimal import Decimal
import arrow


def to_dict(obj):
    """
    :type obj: object
    :rtype: dict
    """
    copy_dict = dict(obj.__dict__)
    for k, v in list(copy_dict.items()):
        if v is None:
            del copy_dict[k]
        elif isinstance(v, arrow.Arrow):
            copy_dict[k] = v.for_json()
    return copy_dict


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
