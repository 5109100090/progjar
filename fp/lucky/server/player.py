
class Player(object):

    def __init__(self, name='', color='', automatic=False):
        self.name = name
        self.color = color
        self.position = 0
        self.automatic = automatic
        self.msg = ''
        self.status = 'I'

    def get_player(self):
        return {'name': self.name,
                'color': self.color,
                'auto': self.automatic}

    def move(self, score):
        self.msg = '%s got a %s....' % (self.name, str(score))
        if not self.position and score != 1:
            self.msg = self.msg + 'but need a 1 to start'
            return (0, 0)
        old_position = self.position
        self.position = old_position + score
        return (old_position, self.position)

