import socket, sys, os, time

#create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#define ip address and port
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#bind
s.bind(ADDR)

#allow 5 simultaneous
s.listen(5)

#welcome
print "welcome, server is ready."

while(1) :
	#accepting new connection
	conn, addr = s.accept()
	
	#receive data
	data = conn.recv(1024)
	
	if data == "off" :
		response = "server turned off. see you.\n"
	elif data == "dir" :
		process = os.popen("ls dir")
		response = str(process.read())
	else :
		#try to split command if exist
		request = data.split()
		
		if request[0] == "get" :
			fname = request[1]
			target = "dir/" + fname
			path = os.path

			#check the file exist or not
			if path.isfile(target) :
				print "response file " + fname + " ..."

				#open file to read
				f = open(target, "r")

				#get file size and split it into packets
				divisor = 1000
				size = int(path.getsize(target))
				split = int(size / divisor)
				mod = int(size % divisor)
				if mod > 0 :
					packet = int(split + 1)
				else :
					packet = split
				
				#send number of packet to be received by client
				conn.send(str(packet))

				#print file and number of packet information
				#print "size : "+str(size)+" split : "+str(split)+" mod : "+str(mod)+" packet : "+str(packet)
				print "size " + str(size) + " byte(s) | " + str(packet) + " packet(s)"

				#send packet every 0.5 second
				for i in range(0, packet) :
					#start point of  packet
					fseek = divisor * i
					f.seek(fseek)

					#end point of packet
					if i == (packet - 1) :
						fread = size
					else :
						fread = divisor
					m = f.read(fread)
					#print m

					#send the packet
					conn.send(m)

					#print sending information
					print "#" + str(i) + " transfer : " + str(fseek) + " to " + str(fread) + " byte(s) "+ str(sys.getsizeof(m))

					#give server some coffe break to send the next packet
					time.sleep(0.5)
	
				print fname + " succesfully sent."
			else :
				#send failure message
				conn.send("-1")
				print fname + " not exist."
		else :
			#bad request
			response = "something wrong with the request.\n"
	
	if (data == "dir" or data == "off") :
		#send request result as response to client
		conn.send(response)
		
		#and print it on server
		print "command : " + data + "\nresponse :\n" + response
		
	#close current connection
	conn.close()
		
	if data == "off" :
		break

#close socket
s.close()
