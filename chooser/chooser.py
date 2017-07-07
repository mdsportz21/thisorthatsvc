import random


class Chooser(object):
    def __init__(self, subjects):
        self.subjects = subjects
        self.last_indices = []

    def choose(self, num_subjects=2):
        total_subjects = len(self.subjects)
        if num_subjects > total_subjects:
            raise ValueError(''.join(['Requested ', num_subjects, ' subjects, but I only have ', total_subjects]))
        elif num_subjects == total_subjects:
            return self.subjects
        else:
            # random!
            condition = True
            while condition:
                indices = random.sample(range(0, total_subjects), 2)
                condition = indices == self.last_indices
            self.last_indices = indices
            return [self.subjects[x] for x in indices]
