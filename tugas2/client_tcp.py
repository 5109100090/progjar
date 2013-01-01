import socket, sys, os, time

#define server address
IPADDR = '127.0.0.1'
PORT = 3000
ADDR = (IPADDR,PORT)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
s.connect((IPADDR, PORT))

#get input
arg1 = sys.argv[1]

#send request
if arg1!="get" :
	s.send(arg1)
else :
	arg2 = sys.argv[2]
	s.send(arg1 + " " + arg2)

#receive message from server
data = s.recv(1024)

if arg1 == "get" :
	if data == "-1" :
		data = "failed to download " + arg2
	else :
		print "receiving packets ..."

		#create and open the file
		f = open(arg2, 'a')

		#receiving packets
		for i in range(0, int(data)) :
			m = s.recv(1024)
			print "#" + str(i) + " recieved : " + str(sys.getsizeof(m)) + " byte(s)"
			#write packet to the file
			f.write(m)

			#waiting server for his coffe break. let's have some tea here
			time.sleep(0.5)

		#successfull message
		data = arg2 + " downloaded."

#print response
print data

#close socket
s.close()
