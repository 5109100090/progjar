#!/usr/bin/env python

import threading
import time
import math

class mythread(threading.Thread):
    def __init__(self, isdaemon):
        threading.Thread.__init__(self)
        self.stoptrigger = threading.Event()
        self.isdaemon = isdaemon
        print 'init'

    def stop(self):
        self.stoptrigger.set()

    def run(self):
        print 'run'
        while not self.stoptrigger.isSet():
            print 'thread', self.isdaemon, 'running'
            time.sleep(1)

mt = mythread('non-daemon')
mt.start()

print 'hi'
