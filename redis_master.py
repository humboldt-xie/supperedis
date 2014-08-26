#!/usr/bin/env python
import socket, select
import traceback
import json

s = socket.socket()
print socket.gethostname();
host = "0.0.0.0";#socket.gethostname()
port = 4999
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

inputs = [s]
sock_infor={}
server_list={};

def init_command(s,info,command):
	print "init command",command
	info['type']=command['type'];
	s.send(json.dumps([{"command":"alive"}])+"\n");

def alive_command(s,info,command):
	print "alive command",info['peername'][0]+":"+command['port'],command
	name=info['peername'][0]+":"+command['port'];
	command['name']=name;
	server_list[name]=command;

def list_command(s,info,command):
	print "list command",command;
	s.send(json.dumps([server_list])+"\n");



commands_list={
	"init":init_command,
	"list":list_command,
	"alive":alive_command,
};

def process_commands(s,info,commands):
	print "process_commands";
	for command in commands:
		cmd="unknow";
		if 'command' in command:
			cmd=command['command'];
		if cmd in commands_list:
			commands_list[cmd](s,info,command);
		else:
			print "unknow command:",command

def command_recv(r,info):
	try:
		info['peername']=r.getpeername()
		data = r.recv(10240)
		info["disconnected"] = not data
		if not info["disconnected"] :
			info['data']=info['data']+data;
	except :
		traceback.print_exc();
		info["disconnected"] = True
	try:
		while info["data"].find("\n")>=0: 
			pos=info["data"].find("\n");
			data=info["data"][0:pos];
			info["data"]=info["data"][pos+1:];
			print pos,data;
			commands=json.loads(data);
			process_commands(r,info,commands);
	except:
		traceback.print_exc();
	

def recv_event(r):
	if r is s:
		c, addr = s.accept()
		print 'Got connection from', addr
		sock_infor[c]={"type":"unknow","protocal":"json","addr":addr,"data":""};
		inputs.append(c);
	else:
		peername="";
		infor={"disconnected":False};
		if not r in sock_infor:
			infor["disconnected"]=True;
		else:
			infor=sock_infor[r];
			command_recv(r,infor);
		if infor["disconnected"]:
			print peername, 'disconnected'
			inputs.remove(r)
			sock_infor.pop(r);

while True:
	rs, ws, es = select.select(inputs, [], [],1.0)
	print sock_infor
	for r in rs:
		try:
			recv_event(r);
		except:
			traceback.print_exc();
