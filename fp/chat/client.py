#!/usr/bin/env python

import socket
import threading
import time

# thread for prompt
class prompt(threading.Thread):
    def __init__(self, s, size, server):
        threading.Thread.__init__(self)
        self.stoptrigger = threading.Event()    # stop trigger 
        self.s = s                              # socket
        self.size = size                        # buffer size
        self.server = server                    # server address

    def stop(self):
        self.stoptrigger.set()                  # stop event

    def run(self):
        while not self.stoptrigger.isSet():     # while not stopped
            i = raw_input(' prompt >> ')
            line = i.split()

            if line[0] == 'username':           # set username
                self.s.send(i)
                username = self.s.recv(size) 
                print ' prompt >> Username Anda adalah ' + username

            elif line[0] == 'list':             # display online buddy        
                self.s.send(i)
                data = self.s.recv(size)
                print ' prompt >>', data

            elif line[0] == 'lroom':
                self.s.send(i)
                data = self.s.recv(size)
                print ' prompt >>', data

            elif line[0] == 'croom':
                self.s.send(i)
                room = self.s.recv(size)
                print ' prompt >> membuat room ' + room

            # set who default source and default destination are
            elif line[0] == 'chat' and line[1] != 'start':
                self.s.send(i)        
                data = self.s.recv(size)
                print ' prompt >> Anda akan chat dengan ' + data + '. Ketik [chat start] untuk memulai chat'

            # start send and receive thread, stop prompt thread
            elif line[0] == 'chat' and line[1] == 'start':
                self.s.send(i)
                send_thread = sendmsg(s, server)
                send_thread.start()
                recv_thread = recvmsg(s, size)
                recv_thread.start()
                self.stop()

            elif line[0] == 'exit':
                self.s.send(i)
                self.stop()
                print 'Thread prompt stopped.'

            else:
                print 'Illegal command.'

class sendmsg(threading.Thread):
    def __init__(self, s, destination):
        threading.Thread.__init__(self)
        self.stoptrigger = threading.Event()
        self.destination = destination
        self.s = s

    def stop(self):
        self.stoptrigger.set()

    def run(self):
        while not self.stoptrigger.isSet():
            msg = raw_input('\r   send >> ')
            if msg == 'exit':
                self.stop()

            # check message length
            if len(msg) == 256:
                print 'Pesan yang dikirimkan melebihi 256 B. Kirim pesan dengan panjang maksimum 256 B.'
            else:
                msg = 'chaton ' + msg
                self.s.sendto(msg, self.destination)
			
class recvmsg(threading.Thread):
    def __init__(self, s, size):
        threading.Thread.__init__(self)
        self.stoptrigger = threading.Event()
        self.s = s

    def stop(self):
        self.stoptrigger.set()

    def run(self):
        while not self.stoptrigger.isSet():
            msg = self.s.recv(size)
            if msg == 'exit':
                self.stop()
            print "\rreceive >>", msg

if __name__ == "__main__":
    server = ('', 6000)
    size = 512 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(server)

    p = prompt(s, size, server)
    p.start()
