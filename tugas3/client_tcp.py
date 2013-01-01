#!/usr/bin/env python

import socket, HttpRequest

#define server address
SERVER = "localhost"
PORT = 80
ADDR = (SERVER, PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
s.connect(ADDR)

#page request
#page = "/page.html"
page = HttpRequest.path

#header request
header = "GET " + page + " HTTP/1.0\r\n\r\n"
#print header
#send request
s.send(header)

#receive message from server
data = s.recv(1024)

#print response
content = data.split("\r\n\r\n")

print "#get header :"
print content[0]
print ""
print "#get body :"
print content[1]

#close socket
s.close()
