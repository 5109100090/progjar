import SimpleXMLRPCServer

from lucky_python import LuckyPython

class ManageObjects(object):

    def __init__(self):
        self.lucky_python = LuckyPython()

    def get(self, type):
        if type == 'board':
            return self.lucky_python.get_board()
        elif type == 'changed_player':
            return self.lucky_python.get_changed_player()
        elif type == 'score':
            return self.lucky_python.get_score()
        elif type == 'turn':
            return self.lucky_python.get_turn()

    def set(self, object):
        type = object['type']
        if type == 'player':
            return self.lucky_python.add_player(object)
        elif type == 'status':     # avilable only for admin user/client
            return self.lucky_python.set_board_status(object)
        elif type == 'score':
            return self.lucky_python.set_score(object)

class LuckyServer(object):

    def __init__(self, port=5678):
        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", port))

    def start(self):
        manage_objects = ManageObjects()
        self.server.register_instance(manage_objects)
        self.server.serve_forever()

if __name__ == "__main__":
    lucky_server = LuckyServer()
    lucky_server.start()
