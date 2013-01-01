#!/usr/bin/env python 

import select 
import socket 
import sys 
import time

backlog = 5 
size = 512 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 5000)) 
server.listen(backlog) 

input = [server, sys.stdin] 
cc = []     # cc = connected client
buddy = []  # buddy list
running = 1
destination = 0
source = 0
    
while running: 
    inputready, outputready, exceptready = select.select(input, [], []) 

    for s in inputready: 
        if s == server: 
            client, address = server.accept()     
            cc.append(address[1])
            print 'Client', address, 'telah terkoneksi'
            input.append(client) 

        elif s == sys.stdin: 
            running = 0 

        else:             
            destination_address = ('', cc[0])
            source_address = ('', cc[1])                

            while 1:
                print 'dest: ', destination_address, 'source: ', source_address
                d = s.recv(size)

                if not d:
                    break

                s.sendto(d, destination_address)

            s.close() 
            input.remove(s) 

server.close()
