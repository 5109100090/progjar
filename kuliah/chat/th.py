#!/usr/bin/env python

import threading
import time
import math

class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event() # stop trigger
        self.num = num
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        while not self.stop_event.isSet():
            print 'hello from thread %d' % self.num
            time.sleep(1)

start = time.time()

mt = MyThread(1)
mt.start()

print 'test 1'

time.sleep(5)
end = time.time()
duration = end - start

if math.floor(duration) == 5:
    mt.stop()

print 'test 2'
