#!/usr/bin/env python 

import select 
import socket 
import sys 
import time

# backlog and buffer size
backlog = 5 
size = 512 

# building socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 6000)) 
server.listen(backlog) 

# incoming socket
input = [server, sys.stdin] 
ca = {}         # ca = connected address
buddy = {}      # dictionary buddy list {address, socket client}
room = {}	# dictionary room list
running = 1     
source = ''     # default source address
destination = ''# default destination address

while running: 
    inputready, outputready, exceptready = select.select(input, [], []) 

    for s in inputready: 
        if s == server: 
            client, address = server.accept()   # accept incoming client     
            ca[address] = client                # add {address, socket client} to dictionary
            input.append(client)                # add socket client to list (for select)
            print 'Client', address, 'telah terkoneksi'

        elif s == sys.stdin: 
            running = 0                         # break condition

        else: 
            data = s.recv(size)                 # received data from client
            addr = s.getpeername()              # addr = client address
            rd = data.split()                   # rd = received data, splitted

            if len(data) == 0:
                running = 0
                sys.exit(1)
            
            # set {username, addr} add to dictionary buddy 
            if rd[0] == 'username' and len(rd) == 2:
                s.send(rd[1])
                buddy[rd[1]] = addr
                print 'Client', addr, 'adalah', rd[1]

            # display online buddy: get buddy key, convert to string
            elif rd[0] == 'list' and len(rd) == 1:
                friends = buddy.keys()
                friends = ', '.join(friends)
                s.send(friends)
                print 'Client', addr, 'menampilkan daftar teman'

	    elif rd[0] == 'croom' and len(rd) == 2:
		s.send(rd[1])
		lr = len(room) + 1
		room[lr] = rd[1]
		print 'Client', addr, 'membuat room', rd[1]

	    elif rd[0] == 'lroom' and len(rd) == 1:
		s.send(str(room))
		print 'Client', addr, 'menampilkan room'

            # chat [username] [username]: set who default source and destination is
            elif rd[0] == 'chat' and rd[1] != 'start' and len(rd) == 3:
                s.send(rd[2])
                source = buddy[rd[1]]
                destination = buddy[rd[2]]
                print 'Client', rd[1], buddy[rd[1]], 'memulai chat dengan', rd[2], buddy[rd[2]] 

            # chat start: trigger for send and recv thread, no big deal for server
            elif rd[0] == 'chat' and rd[1] == 'start' and len(rd) == 2:
                print 'Chat start.', addr
                pass

            # chatting conversation here
            elif rd[0] == 'chaton' and len(rd) >= 2:
                # get incoming message, convert and concat it to one string since it has been splitted
                msg = ' '.join(rd[1:])

                # determine who is current source? who is current destination?
                # if incoming address equal with source
                if addr == source:
                    socker = ca[destination]
                    socker.send(msg)
                    print 'Chat on. source:', source, 'destination:', destination, 'data:', msg

                # if incoming address equal with default destination, swap them 
                elif addr == destination:
                    temp = destination
                    destination = source
                    source = temp

                    # send using socket client, check socket client dictionary first
                    socker = ca[destination]
                    socker.send(msg)
                    print 'Chat on. source:', source, 'destination:', destination, 'data:', msg

            # bye: close socket, remove socket from list
            else:                
                s.close() 
                input.remove(s) 

server.close()
