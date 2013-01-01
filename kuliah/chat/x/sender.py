#!/usr/bin/env python 

import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(('', 5000))

while 1:
    msg = raw_input('>> ')
    if msg == 'exit':
        break
    s.send(msg)
