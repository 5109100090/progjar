import socket

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

#receive message
#input : size
#output : pesan sm ip address

data, addr = s.recvfrom(1024)

#print report
print "terima..."

#send data back to client
s.sendto(data,addr)

#close socket
s.close()
