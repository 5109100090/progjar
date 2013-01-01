#!/usr/bin/env python

import socket
import threading
import sys

class receiver(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
        self.sock = sock

    def stop(self):
        self.stopevent.set()

    def run(self):
        while not self.stopevent.isSet():
            msg = self.sock.recv(512)
            print '\nfriend: ', msg

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 5000))
    s.listen(5)

    client, address = s.accept()
    while 1:
        r = receiver(client)
        r.start()

        msg = raw_input('me: ')
        if msg == 'exit':
            r.stop()
            break
        client.sendto(msg, address)

    r.join()


