import BaseHTTPServer

class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):
    def do_GET( self ):
        self.content()
    def content( self):
	rootdir = "/home/rizky/progjar/tugas3"
	f = file(rootdir+self.path, "r")
	response = f.read()
        self.send( "text/html", response )
    def send( self, type, body ):
        self.send_response( 200 )
        self.send_header( "Content-type", type )
        self.send_header( "Content-length", str(len(body)) )
        self.end_headers()
        self.wfile.write( body )

def httpd(server_address):
    srvr = BaseHTTPServer.HTTPServer(server_address, Handler)
    srvr.handle_request()

if __name__ == "__main__":
    server = ("10.151.36.39", 3000)
    while 1:
        httpd(server)
