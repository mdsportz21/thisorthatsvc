class SubjectDAO(object):
    def __init__(self, mongo):
        self.mongo = mongo

    def store_subjects(self, subjects):
        self.mongo.db.subjects.insert_many(subjects)

    def get_subjects(self):
        return list(self.mongo.db.subjects.find())
