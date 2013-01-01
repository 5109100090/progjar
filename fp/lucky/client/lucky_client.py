import time
import xmlrpclib

class LuckyClient(object):

    board = ''
    player = ''
    server = ''
    def __init__(self):
        pass

    def set_player(self):
        lst_name = ['jayesh', 'jayesh1', 'jayesh2']
        import random
        self.name = lst_name[random.randint(0, 2)]

        self.player = {'type': 'player',
                       'name': self.name,
                       'color': 'black'}
        return self.server.set(self.player)

    def get_turn(self):
        return self.server.get('turn')

    def set_score(self, score_obj):
        value = self.server.set(score_obj)

    def get_changed_player(self):
        return self.server.get('changed_player')

    def get_board(self):
        board = self.server.get('board')
        return board

    def get_my_score(self):
        raw_input("This is your turn....Press Enter to throw !!")
        return self.server.get('score')

    def connect(self, server='127.0.0.1', port='5678'):
        """ """
        self.server = xmlrpclib.ServerProxy(server)

    def start(self):
        """ """
        self.connect(server='http://127.0.0.1:5678', port='5678')
        result = self.set_player()
        if not result:
            raise AttributeError, 'Name already in use'
        self.play()

    def play(self):
        """ """
        while 1:
            time.sleep(1)
            self.board = self.get_board()

            #self.drow_board()  #drow self.board in the way u want
            if self.board['status'] == 'P':
                print self.board['msg']
                break

        while 1:
            time.sleep(1)
            turn_name = self.get_turn()
            score = 0

            changed_player = self.get_changed_player()
            if changed_player:
                print changed_player['msg']  #FIXME
            if changed_player and changed_player['status'] == 'W':
                break
            #self.redrow_board()  #re drow
            if turn_name == self.name:
                score = self.get_my_score()
                score_object = {'type': 'score', 'name': self.name,
                                 'score': score}
                self.set_score(score_object)

if __name__ == "__main__":
    luckypy = LuckyClient()
    luckypy.start()
