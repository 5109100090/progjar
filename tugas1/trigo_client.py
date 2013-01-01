import socket

#define server address
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
	inp = raw_input("masukkan angka: ")
	
	#send message to server
	s.sendto(inp,ADDR)
	
	if inp == '#':
		break

	#receive message from server
	#sin,addr = s.recvfrom(1024)
	#cos,addr = s.recvfrom(1024)
	#tan,addr = s.recvfrom(1024)
	a,addr = s.recvfrom(1024)
	
	#print report
	print "angka : " + inp
	#print "sin : " + sin
	#print "cos : " + cos
	#print "tan : " + tan
	print a

#close socket
s.close()
