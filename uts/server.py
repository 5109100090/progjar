import socket
import threading

BUFFER = 256

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

s.listen(5)

#user dictionary
user = {}

class TSend(threading.Thread):

    def __init__(self,c,a):
        threading.Thread.__init__(self)
        self.conn=c
	self.addr=a
	#self.start=1
    
    def run(self):
	#while self.start :
	print "tes"
	msg = self.conn.recv(BUFFER)
	print "msg : " + msg + " addr : "+str(addr)
	self.conn.send(msg)
	
while 1 :
	#accepting new connection
	conn, addr = s.accept()

	#receive username
	data = conn.recv(1024)
	msg = data.split(" ")
	if msg[0] == "exit" :
		#thr.start=False
		#thr.conn.close()
		break
	elif msg[0] == "username" :
		user[msg[1]] = str(addr)
		print user

		thr = TSend(conn, addr)
		thr.start()
		#thr.join()

#close socket
conn.close()
s.close()
