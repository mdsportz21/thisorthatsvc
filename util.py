def to_dict(obj):
    """
    :type obj: object
    :return: dict
    """
    copy_dict = dict(obj.__dict__)
    for k, v in list(copy_dict.items()):
        if v is None:
            del copy_dict[k]
    return copy_dict
