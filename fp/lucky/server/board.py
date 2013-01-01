from player import Player
from snake import Snake
from ladder import Ladder

class Board(object):

    def __init__(self, no_of_rows=10, no_of_columns=10,
                 snakes_conf=(), ladders_conf=(), die=''):
        self.die = die
        self.no_of_rows = no_of_rows
        self.no_of_columns = no_of_columns

        self.play_turn = ''
        self.active_player = ''
        self.play_order = []

        self.players = {}
        self.snakes = {}
        self.ladders = {}
        self.status = 'N'   #New
        self.msg = ''
        self.snakes_conf = snakes_conf
        self.ladders_conf = ladders_conf

        for each_snake in snakes_conf:
            self.add_snake(Snake(each_snake[0], each_snake[1]))
        for each_ladder in ladders_conf:
            self.add_ladder(Ladder(each_ladder[0], each_ladder[1]))

    def add_player(self, player_object):
        if player_object['name'] in self.players:
            return False
        player = Player(name=player_object['name'],
                        color=player_object['color'])
        self.players[player.name] = player

        self.play_order.append(player_object['name'])
        if len(self.players) == 3:     #FIXME
            self.play_turn = self.play_order[0]
            self.msg = 'Game stated !!'
            self.status = 'P'
        return True

    def add_snake(self, snake):
        self.snakes[snake.start_column] = snake

    def add_ladder(self, ladder):
        self.ladders[ladder.start_column] = ladder

    def get_board(self):
        dct_board = {}
        lst_players = []
        for key, value in self.players.iteritems():
            lst_players.append(value.get_player())

        dct_board = {'no_of_rows': self.no_of_rows,
                     'no_of_columns': self.no_of_columns,
                     'players': lst_players,
                     'snakes': self.snakes_conf,
                     'ladders': self.ladders_conf,
                     'status': self.status,
                     'msg': self.msg}
        return dct_board

    def get_turn(self):
        return self.play_turn

    def get_active_player(self):
        if not self.active_player:
            return ''
        player = self.players[self.active_player]
        return {'position': player.position,
                'status': player.status,
                'msg': player.msg,
                'name': player.name}

    def set_score(self, score_object):
        player = self.players[score_object['name']]
        score = score_object['score']
        player.msg = ''
        (old_position,
         new_position) = player.move(score)
        if new_position == self.no_of_rows * self.no_of_columns:
            player.status = 'W'
            player.msg = player.msg + '\n%s wins !!!' % player.name

        if new_position > self.no_of_rows * self.no_of_columns:
            player.msg = player.msg +  '\nThis is more than %s want !!' % player.name
            player.position = old_position

        if new_position in self.snakes:
            self.snakes[new_position].bite(player)

        if new_position in self.ladders:
            self.ladders[new_position].climb(player)

        player.msg = player.msg + "\n %s's new position is %s" % (player.name,
                                                                  player.position)
        self.active_player = player.name

        if score != self.die.no_of_faces:
            self.play_turn = self.play_order[(self.play_order.index(self.play_turn) + 1) \
                                                 % len(self.play_order)]
        else:
            player.msg = player.msg + '\n %s got a maximum so one more chance' % player.name
        return True
