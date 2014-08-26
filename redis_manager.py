#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import sep, curdir
import socket
import cgi
PORT = 8000
class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		endwith={".css":"text/css",".html":"text/html",".jpg":"image/jpg",".js":"application/javascript",'.txt':'text/txt'};
		try:
			curpath=curdir + sep + "views" 
			if self.path=="/":
				self.path="/index.html"
			reply = False
			for i in endwith:
				if self.path.endswith(i):
					reply=True;
					mimeType=endwith[i];
			if(reply == True):
				fp = open(curpath + sep + self.path)
				self.send_response(200)
				self.send_header('content-type', mimeType)
				self.end_headers()
				self.wfile.write(fp.read())
				fp.close()
				return
		except IOError:
			self.send_error(404, 'Not Found File %s' %self.path);
		print self.path;
	def do_POST(self):
		print "post";
		remainbytes = int(self.headers['content-length'])
		command=self.rfile.read(remainbytes )
		print command;
		ip="127.0.0.1";
		port=4999;
		print "connect";
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		sock.connect((ip, int(port)));
		sock.send(command+"\n");
		buffer=sock.recv(10240);
		sock.close();
		self.send_response(200)
		self.send_header('content-type', "text/json")
		self.send_header('content-length', len(buffer))
		self.end_headers()
		self.wfile.write(buffer);



#SimpleHTTPServer.SimpleHTTPRequestHandler
server = HTTPServer(('', PORT), RequestHandler)
print 'started httpserver...'
server.serve_forever()
