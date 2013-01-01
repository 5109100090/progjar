#!/usr/bin/env python 

import socket 
import threading
import sys

class receiver(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
        self.s = s

    def stop(self):
        self.stopevent.set()

    def run(self):
        while not self.stopevent.isSet():
            msg = self.s.recv(512)
            print '\nfriend:', msg

class sender(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
        self.s = s

    def stop(self):
        self.stopevent.set()

    def run(self):
        while not self.stopevent.isSet():
            msg = raw_input('me: ')
            if msg == 'exit':
                self.stop()
            self.s.sendto(msg, ('', 5000))

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('', 5000))
    
    r = receiver(s)
    r.start()
    s = sender(s)
    s.start()
