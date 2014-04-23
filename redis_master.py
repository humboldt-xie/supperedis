#!/usr/bin/env python
import socket, select

s = socket.socket()
print socket.gethostname();
host = "0.0.0.0";#socket.gethostname()
port = 4999
s.bind((host, port))

s.listen(5)
inputs = [s]
while True:
	rs, ws, es = select.select(inputs, [], [],1.0)
	print(".");
	for r in rs:
		if r is s:
			c, addr = s.accept()
			print 'Got connection from', addr
			inputs.append(c)
			#c.send("command=alive\n");
		else:
			peername="";
			try:
				peername=r.getpeername()
				data = r.recv(1024)
				disconnected = not data
				#r.send("command=alive\n");
			except socket.error:
				disconnected = True

			if disconnected:
				print peername, 'disconnected'
				inputs.remove(r)
			else:
				print data

