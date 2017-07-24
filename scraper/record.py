class Selector(object):
    """
    :type tag_name: str
    :type class_name: str
    """
    def __init__(self, tag_name, class_name=None, sub_tag_name=None):
        self.tag_name = tag_name
        self.class_name = class_name
        self.sub_tag_name = sub_tag_name
