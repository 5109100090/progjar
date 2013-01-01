from board import Board
from die import Die

class LuckyPython(object):

    def __init__(self, conf={}):
        conf = self.get_conf_values()
        self.die = Die(no_of_faces=conf['no_of_faces_of_die'])
        self.board = Board(no_of_rows=conf['no_of_rows'],
                           no_of_columns=conf['no_of_columns'],
                           snakes_conf=conf['snakes'],
                           ladders_conf=conf['ladders'],
                           die=self.die)

    def get_board(self):
        return self.board.get_board()

    def get_changed_player(self):
        return self.board.get_active_player()

    def get_score(self):
        score = self.die.get_score()
        return score

    def add_player(self, object):
        return self.board.add_player(object)

    def set_board_status(self, object):
        if object['status'] == 'start':
            self.board.msg = 'Starting the game'
            self.board.status = 'P'  #start play

    def set_score(self, score_object):
        return self.board.set_score(score_object)

    def get_turn(self):
        return self.board.get_turn()

    def get_conf_values(self):
        """ get from user """ #FIXME
        conf_dict =  {'no_of_columns': 10,
                      'no_of_rows': 10,
                      'snakes': ((20, 10), (40, 6), (66, 33), (98, 18)),
                      'ladders': ((5, 14), (32, 62), (46, 58), (60, 84)),
                      'no_of_faces_of_die': 6}
        return conf_dict
