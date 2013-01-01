import socket, threading

#define server address
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
s.connect((IPADDR, PORT))

class TRecv(threading.Thread):
	def __init__(self,s):
		threading.Thread.__init__(self)
		self.conn = s
	
	def run(self):
		msg = self.conn.recv(1024)
		print msg

#send message
uname = raw_input();
s.send(str(uname))

thr = TRecv(s)
thr.start()
#thr.join()

#msg = s.recv(1024)
#print msg
#close socket
s.close()
