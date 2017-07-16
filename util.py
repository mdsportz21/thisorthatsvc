from decimal import Decimal


def to_dict(obj):
    """
    :type obj: object
    :rtype: dict
    """
    copy_dict = dict(obj.__dict__)
    for k, v in list(copy_dict.items()):
        if v is None:
            del copy_dict[k]
    return copy_dict


def divide(a, b, precision=4):
    """
    :type a: float
    :type b: float
    :type precision: int
    :rtype: float
    """
    return float((a / Decimal(b)).quantize(Decimal('1e-' + str(precision))))
