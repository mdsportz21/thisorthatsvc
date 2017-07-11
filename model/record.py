from bson.objectid import ObjectId


class SubjectRecord(object):
    """
    :type _id: ObjectId
    :type img_desc: str
    :type description: str
    :type img_link: str
    :type next_subject_id: ObjectId
    :type NEXT_SUBJECT_ID_FIELD: str
    """

    NEXT_SUBJECT_ID_FIELD = '_next_subject_id'

    def __init__(self, _id=None, img_desc=None, description=None, img_link=None, next_subject_id=None):
        self._id = _id
        self._img_desc = img_desc
        self._description = description
        self._img_link = img_link
        self._next_subject_id = next_subject_id

    @staticmethod
    def subject_record_factory(subject_record_dict):
        subject = SubjectRecord()
        subject.update(**subject_record_dict)
        return subject

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def img_desc(self):
        return self._img_desc

    @img_desc.setter
    def img_desc(self, value):
        self._img_desc = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, value):
        self._img_link = value

    @property
    def next_subject_id(self):
        return self._next_subject_id

    @next_subject_id.setter
    def next_subject_id(self, value):
        self._next_subject_id = value


class SubjectRecordDict(object):
    """
    :type subject_records: list of SubjectRecord
    :type subject_records_dict: dict[ObjectId, SubjectRecord]
    :type id_to_prev_subjects: dict[ObjectId, list[SubjectRecord]]
    :type subjects_with_no_next: list of SubjectRecord
    :type ids_without_prev: set of ObjectId
    """

    def __init__(self, subject_records):
        self.subject_records = subject_records
        self.subject_records_dict = {record.id: record for record in subject_records}
        # subjects grouped by nextSubjectId
        self.subjects_with_no_next = []
        self.subjects_with_next = []
        self.id_to_prev_subjects = {}
        self.ids_without_prev = set([subject_record.id for subject_record in subject_records])
        for subject_record in subject_records:
            next_subject_id = subject_record.next_subject_id
            if next_subject_id is not None:
                if next_subject_id not in self.id_to_prev_subjects:
                    self.id_to_prev_subjects[next_subject_id] = []
                self.id_to_prev_subjects[next_subject_id].append(subject_record)
                self.subjects_with_next.append(subject_record)
                if next_subject_id in self.ids_without_prev:
                    self.ids_without_prev.remove(next_subject_id)
            else:
                self.subjects_with_no_next.append(subject_record)

    def get_prev_subjects(self, subject_record_id):
        """
        :type subject_record_id: ObjectId
        :rtype: list of SubjectRecord
        """
        return self.id_to_prev_subjects[subject_record_id] if subject_record_id in self.id_to_prev_subjects else []

    def get_subjects_with_same_next(self):
        """
        Get the first list of subjects whose next are the same, or None
        :rtype: list of SubjectRecord
        """
        for next_id, subjects_with_next in self.id_to_prev_subjects.iteritems():
            if len(subjects_with_next) > 1:
                return subjects_with_next

        return None

    def get_next(self, subject_record):
        """
        :type subject_record: SubjectRecord
        :rtype: SubjectRecord
        """
        return self.subject_records_dict[subject_record.next_subject_id] \
            if subject_record is not None \
               and subject_record.next_subject_id is not None \
               and subject_record.next_subject_id in self.subject_records_dict \
            else None

    def get(self, subject_id):
        """
        :type subject_id: ObjectId
        :rtype: SubjectRecord
        """
        return self.subject_records_dict[subject_id]

    def get_subjects_with_no_next(self):
        """
        Gets subjects with no next
        :rtype: list of SubjectRecord
        """
        return self.subjects_with_no_next

    def get_subjects_with_next(self):
        """
        Gets subjects with a next
        :rtype: list of SubjectRecord
        """
        return self.subjects_with_next

    def is_greater(self, subject_id_one, subject_id_two):
        """
        :type subject_id_one: ObjectId
        :type subject_id_two: ObjectId
        :rtype: bool
        """
        subject_one_record = self.get(subject_id_one)
        subject_two_record = self.get(subject_id_two)
        if subject_two_record.next_subject_id is None:
            return True
        elif subject_one_record.next_subject_id is None:
            return False
        else:
            while subject_one_record is not None:
                if subject_one_record.next_subject_id == subject_id_two:
                    return True
                subject_one_record = self.get_next(subject_one_record)
            return False

    def get_subject_ids_with_no_prev(self):
        """
        :rtype: set of ObjectId
        """
        return self.ids_without_prev

    def get_subject_records(self):
        """
        :rtype: list of SubjectRecord
        """
        return self.subject_records
