import random

class Die(object):

    def __init__(self, no_of_faces=6):
        self.no_of_faces = no_of_faces

    def get_score(self):
        score = random.randint(1, self.no_of_faces)
        return score
