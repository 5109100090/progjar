import socket

#define server address
IPADDR = '127.0.0.1'
PORT = 50000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
s.connect((IPADDR, PORT))

#send message
s.send("Hai john")

#receive message from server
data = s.recv(1024)

#print report
print data

#close socket
s.close()
