
class Snake(object):

    def __init__(self, start_column, end_column):
        if int(start_column) <= int(end_column):
            raise AttributeError, "End should be smaller than start"
        self.start_column = start_column
        self.end_column = end_column

    def bite(self, player):
        msg = '..ha..ha.. ha.. Thanks for %s, for being my pray !\n' % player.name
        player.msg = player.msg + msg
        player.position = self.end_column
