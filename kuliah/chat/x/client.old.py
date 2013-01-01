#!/usr/bin/env python 

import socket 
import sys 
import thread

def client_send(s, addr):
    while 1:
        msg = raw_input('send >> ')
        if msg == 'exit':
            s.close()
            break
        s.sendto(msg, addr)

def client_recv(s, size):
    while 1:        
        msg = s.recv(size)
        print msg

addr = ('', 5000)
size = 512 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(addr)
username = ''

while 1: 
    i = raw_input('client >> ')
    line = i.split()
    
    if line[0] == 'username':
        s.send(i)
        data = s.recv(size) 
        username = data
        print '>> Username Anda adalah ' + data

    elif line[0] == 'list':        
        s.send(i)
        data = s.recv(size)
        print '>>', data

    elif line[0] == 'chat' and line[1] != 'start':
        s.send(i)        
        data = s.recv(size)
        print '>> Anda akan chat dengan ' + data + '. Ketik [chat start] untuk memulai chat'

    elif line[0] == 'chat' and line[1] == 'start':
        s.send(i)

        thread.start_new_thread(client_send, (s, addr))
        thread.start_new_thread(client_recv, (s, size))
        break
