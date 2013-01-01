import socket
import sys

#define server address
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#get argumen
inp = sys.argv[1]

#send message to server
s.sendto(inp,ADDR)

#get data from server
data,addr = s.recvfrom(1024);

#print data
print data

#close socket
s.close()
