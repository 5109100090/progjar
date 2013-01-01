#!/usr/bin/env python
 
# mengimpor modul socket
import socket
import os
import sys
 
# menentukan alamat server
server_address = ('localhost', 5000)
 
# ukuran buffer ketika menerima pesan
SIZE = 1024
 
# membuat objek socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# menggunakan kembali alamat 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# bind ke alamat server
s.bind(server_address)
 
# mendengarkan koneksi dari client
s.listen(5)
 
# siap menerima pesan terus-menerus dari client
while 1:
    try:
        # menerima koneksi dari client
        client, client_address = s.accept()

        # menerima pesan dari client
        message = client.recv(SIZE)
        print message

        # jika tidak ada pesan, keluar dari while
        if not message:
            break
        
        # /var/www-like
        varwww = "/home/hudan/Py/tugas03"

        # mendapatkan request file
        request_header = message.split('\r\n')
        request_line = request_header[0]
        request_file = request_line.split()[1]

        # menyusun absolute path
        if request_file == "/":
            request_file = varwww + "/index.html"
        else:
            request_file = varwww + request_file

        # cek apakah file ada. 
        # jika ada: 200 OK
        if os.path.exists(request_file):
            # file size
            file_size = str(os.path.getsize(request_file))

            # menyusun response header
            response_header = "HTTP/1.1 200 OK\r\nServer: pyHTTPServ 1.0\r\nContent-length: " + file_size + "\r\n\r\n"

            # membuka request file
            f = open(request_file, 'rb')
            response_content = f.read()
            f.close()

        # jika tidak ada: 404 Not Found
        else:
            response_header = "HTTP/1.1 404 Not Found\r\nServer: pyHTTPServ 1.0\r\n\r\n"
            response_content = "<html><body><h1>404 Not Found</h1></body></html>"

        # mengirimkan kembali pesan ke client
        client.send(response_header + response_content)
        client.close()
    
    except(KeyboardInterrupt, SystemExit):
        sys.exit(0)

# menutup socket
s.close()
