import socket

#define server address
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send message to server
#param : pesan, alamat server
s.sendto("Hai john",ADDR)

#receive message from server
data,addr = s.recvfrom(1024)

#print report
print data

#close socket
s.close()
