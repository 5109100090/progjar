#!/usr/bin/env python
import select, socket, sys, threading

class game(threading.Thread):
	def __init__(self, ca, buddy, room, croom):
		threading.Thread.__init__(self)
		self.s = s
		self.ca = ca
		self.buddy = buddy
		self.room = room
		self.croom = croom
		self.step = {}
		self.box = {}
		self.nbox = 100
		self.winner = ''
		self.stoptrigger = threading.Event()
	
	def stop(self):
		self.stoptrigger.set()
	
	def is_number(self,test):
		try:
			int(test)
			return 1
		except ValueError:
			return 0
	
	def broadcast(self, m):
		for x in self.room[self.croom] :
			temp = self.ca[self.buddy[x]]
			temp.send(m)

	def init_game(self):
		#initiate step of player
		for x in self.room[self.croom] :
			self.step[x] = 0
		
		#initiate board
		self.box[6] = 34
		self.box[8] = 12
		self.box[10] = 28
		self.box[37] = 70
		
		self.box[80] = 70
		self.box[48] = 21
	
	def check_winner(self):
		for x in self.step :
			if self.step[x] >= self.nbox:
				self.winner = x
				m = 'The winner of ' + self.croom + ' is ' + x
				self.broadcast('FINISH###' + m)
				print m
				return 1
		return 0

	def run(self):
		self.init_game()
		while not self.stoptrigger.isSet():
			for x in self.room[self.croom] :
				temp = self.ca[self.buddy[x]]
				self.broadcast("BROADCAST###" + x + "'s playing. ")
				temp.send("PLAY###Press [r] to roll the dice >")
				
				#get dice number
				dice = temp.recv(1024)
				if self.is_number(dice) == 0:
					dice = 0
				self.step[x] = self.step[x] + int(dice)
				
				# cek ada ular atau tangga
				onbox = 0
				for i in self.box.keys():
					if self.step[x] == i:
						onbox = 1	#there's something in the box
						if i > self.box[i] :
							type = 'SNAKE'
						else:
							type = 'LADDER'
						
						tstep = self.step[x]		#current step
						self.step[x] = self.box[i]	#new step
						break
				
				#create message
				m = x + ' move ' + dice + ' step.'
				if onbox == 1:
					m = m + ' ' + type + ' on ' + str(tstep) + ', go to ' + str(self.step[x]) + '.'
				m = m + ' Position : ' + str(self.step[x])
				
				#broadcast message
				self.broadcast("BROADCAST###" + m)
				print m
				
				#check winner
				if self.check_winner() == 1:
					self.stop()
					break

class server:
	def __init__(self):
		self.host = '10.151.36.39'
		self.port = 6000
		self.backlog = 5
		self.size = 1024
		self.server = None
		self.ca = {}
		self.buddy = {}
		self.room = {}
		self.stoptrigger = threading.Event()
	
	def stop(self):
		self.stoptrigger.set()
	
	def open_socket(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((self.host,self.port))
			self.server.listen(5)
		except socket.error, (value,message):
			if self.server:
				self.server.close()
			print "Could not open socket: " + message
			sys.exit(1)
	
	def get_buddy(self, addr):
		for x in self.buddy:
			if self.buddy[x] == addr:
				return x
		return -1
	
	def broadcast_room(self, croom, m):
		for x in self.room[croom]:
			temp = self.ca[self.buddy[x]]
			temp.send(m)
	
	def run(self):
		self.open_socket()
		input = [self.server,sys.stdin]
		while not self.stoptrigger.isSet():
			inputready,outputready,exceptready = select.select(input,[],[])
			for s in inputready:
				if s == self.server:
					conn, addr = self.server.accept()
					print str(addr) + ' connected'
					input.append(conn)
					self.ca[addr] = conn
				elif s == sys.stdin:
					junk = sys.stdin.readline()
					running = 0 
				else :
					data = s.recv(self.size)
					addr = s.getpeername()
					line = data.split()	
					if line[0] == 'user' and len(line) == 2 :
						self.buddy[line[1]] = addr
						m = 'welcome ' + line[1] + ' from ' + str(addr)
						print m
						s.send(m)
					elif line[0] == 'create' and len(line) == 2 :
						user = self.get_buddy(addr)
						if user != -1:
							list = []
							list.append(user)
							self.room[line[1]] = list
							m = user + ' create room ' + line[1]
							print m
						else:
							m = 'invalid'
						s.send(m)
					elif line[0] == 'join' and len(line) == 2 :
						user = self.get_buddy(addr)
						if user != -1:
							self.room[line[1]].append(user)
							m = 'welcome ' + user +' on '+ line[1]
							self.broadcast_room(line[1], m)
							print m
						else:
							m = 'invalid'
							s.send(m)
					elif line[0] == 'buddy' and len(line) == 1 :
						user = self.buddy.keys()
						m = ', '.join(user)
						m = 'online buddies : ' + m
						s.send(m)
					elif line[0] == 'room' and len(line) == 1 :
						room = self.room.keys()
						m = ', '.join(room)
						m = 'available room : ' + m
						s.send(m)
					elif line[0] == 'room' and len(line) == 2 :
						user = self.room[line[1]]
						m = ', '.join(user)
						m = 'buddies on ' + line[1] + ' : ' + m
						s.send(m)
					elif line[0] == 'leave' and len(line) == 2 :
						user = self.get_buddy(addr)
						if user != -1:
							m = user + ' leaving ' + line[1]
							self.broadcast_room(line[1], m)
							l = self.room[line[1]]
							l.remove(user)
							print m
						else:
							m = 'invalid'
							s.send(m)
					elif line[0] == 'start' and len(line) == 2 :
						creator = self.room[line[1]][0]
						creator_addr = self.buddy[creator]
						if creator_addr == addr:
							m = 'Game ' + line[1] + ' started'
							self.broadcast_room(line[1], 'START###' + m)
							print m
							g = game(self.ca, self.buddy, self.room, line[1])
							g.start()
							#self.stop()
						else :
							m = "Invalid. You're not the " + line[1] + " creator"
							s.send(m)
					elif line[0] == 'exit' :
						m = 'exit'
						s.send(m)
					else :
						m = 'bad operand'
						s.send(m)

		# close all threads
		#self.server.close()

if __name__ == "__main__":
	s = server()
	s.run()