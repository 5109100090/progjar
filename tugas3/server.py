#!/usr/bin/env python
import socket, os

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#define ip address and port
IPADDR = '10.151.36.39'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

#allow 5 simultaneous
s.listen(5)

os.system("clear")
rootdir = "/home/rizky/progjar/tugas3/htdocs"

print "web server is running"

while 1 :
	#accepting new connection
	conn, addr = s.accept()
	
	#get request
	data = conn.recv(1024)
	print data
	resp = data.split(" ")
	req = rootdir + resp[1]
	
	path = os.path
	if path.isfile(req) :
		#open requested file
		f = file(req, "r")

		#response message
		header = "HTTP/1.0 200 OK\r\nContent-Type: text/html"
		content = f.read()
		f.close()
	else :
		#response message
		header = "HTTP/1.0 404 Not Found"
		content = "Page Not Found"

	data = header +"\r\n\r\n"+content
	#send response
	conn.send(data)

	print "request "+resp[1]+" from "+str(addr)+" status "+header

	#close socket
	conn.close()

s.close()
