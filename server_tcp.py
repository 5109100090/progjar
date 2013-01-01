import socket

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

#allow 5 simultaneous
s.listen(5)

#accepting new connection
conn, addr = s.accept()

#receive data
data = conn.recv(1024)

if data:
	message = "message : " + data
	print message
	conn.send(message)
else:
	print "something wrong"

#close socket
conn.close()
s.close()
