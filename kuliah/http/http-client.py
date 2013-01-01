#!/usr/bin/env python

import socket
from HTMLParser import HTMLParser

class parse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)       
        self.mylist = []
        self.image = ''

    def handle_starttag(self, tag, attrs):
        self.mylist.append(tag)
        if tag == 'img':
            for a in attrs:
                if a[0] == 'src':
                    self.image = a[1]

    def handle_endtag(self, tag):
        starttag = self.mylist[len(self.mylist)-2]
        data = self.mylist[len(self.mylist)-1]
        
        if tag == 'a' and data != 'span':
            print '[a]', data, '[a]'
        elif tag == 'img':
            print '[img]', self.image, '[img]'
        elif tag == starttag and tag != 'script' and tag!= 'div' and tag != 'span' and data != 'span' and data != 'img':
            print data

    def handle_data(self, data):
        self.mylist.append(data)

# buffer size
SIZE = 1024

# building socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 80))

# arrange request header
req_header = "GET index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

# send request header
s.send(req_header)
ret = ''

# receive response
while True:
    data = s.recv(SIZE)
    if not data:
        break
    ret = ret + data

# split response header and content
d = ret.split('\r\n\r\n')
content = ''.join(d[1:])

# parse
p = parse()
p.feed(content)

# close socket
s.close()
