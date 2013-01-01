import socket
import math

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

while 1:
	#receive input
	data, addr = s.recvfrom(1024)
	print data
	
	if data == '#':
		break
	
	#create math
	m = math
	
	#calculate
	sin = m.sin(m.radians(float(data)))
	cos = m.cos(m.radians(float(data)))
	tan = m.tan(m.radians(float(data)))
	
	#print result
	print sin
	print cos
	print tan

	a = 'sin : '+ str(sin)+ '\ncos : ' + str(cos) + '\ntan : ' + str(tan)
	
	#send data back to client
	#s.sendto(str(sin),addr)
	#s.sendto(str(cos),addr)
	#s.sendto(str(tan),addr)
	s.sendto(a,addr)
	
#close socket
s.close()
