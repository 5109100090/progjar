#!/usr/bin/env python

import httplib, sys, htmllib, os, formatter, string

argv_len = len(sys.argv)
if argv_len != 2 :
	print "usage : ./request_http.py [address]"
	print "ex : ./request_http.py its.ac.id"
else :
	class Parser(htmllib.HTMLParser):
	    # return a dictionary mapping anchor texts to lists
	    # of associated hyperlinks
	
	    def __init__(self, verbose=0):
	        self.anchors = {}
	        f = formatter.NullFormatter()
	        htmllib.HTMLParser.__init__(self, f, verbose)
	
	    def anchor_bgn(self, href, name, type):
	        self.save_bgn()
	        self.anchor = href
	
	    def anchor_end(self):
	        text = string.strip(self.save_end())
	        if self.anchor and text:
	            self.anchors[text] = self.anchors.get(text, []) + [self.anchor]

	connection  = httplib.HTTPConnection(sys.argv[1])
	connection.request("GET","/")
	response = connection.getresponse()
	header = response.getheaders()
	
	print "Status: ", response.status, response.reason
	#print "Response header :"
	#for  item in header :
	#	print item

	#print "Content : ", response.read()
	
	w = formatter.DumbWriter()
	f = formatter.AbstractFormatter(w)
	p = htmllib.HTMLParser(f)
	p.feed(response.read())
	p.close()
	
	print
	print
	#i = 1	
	#for link in p.anchorlist :
	#	print i, "=>", link
	#	i+=1
	
	#os.system("rm temp.html")
