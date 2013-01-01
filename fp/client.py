#!/usr/bin/env python 
import socket, random, threading, time

class game(threading.Thread):
	def __init__(self,s):
		threading.Thread.__init__(self)
		self.s = s
		self.stoptrigger = threading.Event()

	def stop(self):
		self.stoptrigger.set()

	def run(self):
		while not self.stoptrigger.isSet():
			running = 1
			while running :
				#print 'waiting response from server ...'
				msg = self.s.recv(1024)
				rd = msg.split('###')
				if rd[0] == 'BROADCAST':
					print rd[1]
				elif rd[0] == 'PLAY' :
					print rd[1]
					msg = raw_input()
					if msg == 'r' :
						msg = str(random.randint(1,6))
					self.s.send(msg)

				#if msg == 'exit':
				#	self.stop()

class recv(threading.Thread):
	def __init__(self,s,sen):
		threading.Thread.__init__(self)
		self.s = s
		self.sen = sen
		self.stoptrigger = threading.Event()
	
	def stop(self):
		self.stoptrigger.set()
	
	def run(self):
		while not self.stoptrigger.isSet():
			msg = self.s.recv(1024)
			rd = msg.split('###')
			#if rd[0] == 'start' :
			#	print rd[1]
			#	self.stop()
			#	self.sen.stop()
			#	g = game(self.s)
			#	g.start()
			#	break
			
			if rd[0] == 'FINISH':
				print rd[1]
				self.s.close()	#close socket
				self.sen.stop()	#stop send thread
				self.stop()		#stop this thread
				break
			if msg == 'exit':
				print 'bye.'
				self.sen.stop()
				self.stop()
			elif len(rd) == 1:
				print msg
			elif len(rd) == 2:
				print rd[1]

class send(threading.Thread):
	def __init__(self,s):
		threading.Thread.__init__(self)
		self.s = s
		self.stoptrigger = threading.Event()

	def stop(self):
		self.stoptrigger.set()

	def run(self):
		while not self.stoptrigger.isSet():
			msg = raw_input()
			if msg == 'r' :
				msg = str(random.randint(1,6))
				print 'dice : ' + msg
			elif msg == 'exit':
				self.stop()
			else:
				m = 0

			self.s.send(msg)

if __name__ == "__main__":
	IP = '10.151.36.39'
	PORT = 6000
	ADDR = (IP,PORT)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(ADDR)

	sen = send(s)
	sen.start()
	rec = recv(s, sen)
	rec.start()