
class Ladder(object):

    def __init__(self, start_column, end_column):
        if int(end_column) <= int(start_column):
            raise AttributeError, "Start should be smaller than end"
        self.start_column = start_column
        self.end_column = end_column

    def climb(self, player):
        msg = 'ooooo... %s got a short cut !!!\n' % player.name
        player.msg = player.msg + msg
        player.position = self.end_column
