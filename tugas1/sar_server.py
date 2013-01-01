import socket
import os

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

#receive input
data, addr = s.recvfrom(1024)
print data

if data == 'cpu':
	os.system("sar -u 1 3 | awk '{ print $1, $4 }' > file")
	f = os.popen("cat file")
	r = f.read()
elif data == 'mem':
	os.system("sar -r 1 3 | awk '{ print $1 $4 }' > file")
	f = os.popen("cat file")
	r = f.read()
else:
	os.system("sar -r 1 > sar_all")

#os.system("rm file")

#send data back to client
print r
s.sendto(str(r),addr)
#close socket
s.close()
