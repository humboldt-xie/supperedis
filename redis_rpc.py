#!/usr/bin/env python
import os
import time
import socket

def gen_conf(path,setting,template):
	if os.path.exists(path):
		open(path+time.strftime(".%Y-%m-%d_%H:%M:%S",time.localtime()), "wb").write(open(path, "rb").read());
	tpath="./redis_template/%s.conf"%template;
	if not os.path.exists(tpath):
		return False,"type=template_not_found;value=%s"%template;
	file=open(path,"w");
	for  i in open(tpath).readlines() :
		if i[0]=='#':
			file.write(i);
		else:
			list=i.split(" ");
			if list[0] in setting :
				file.write("%s %s\n"%(list[0],setting[list[0]]));
			else:
				file.write(i);
	return True,"type=ok";
def send_redis(ip,port,cmds):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	try:
		sock.connect(("127.0.0.1", int(port)));
	except socket.error,msg:
		return "",msg[0];
	sock.settimeout(2);
	sock.send(cmds);
	recv=sock.recv(1024);
	sock.close();
	return recv,0;

def ping_redis(ip,port):
	 res,msg=send_redis("127,0.0.1",port,"ping\r\n");
	 print [res,msg];
	 if res=="+PONG\r\n" :
		 return True;
	 return False;

def run_redis(request):
	if len(request)<2 :
		return False,"type=args_not_found;value=1";
	args=request[0];
	template="default";
	if "template" in args:
		template=args['template'];
	config_path="";
	setting=request[1];
	port=0;
	if "port" in setting:
		port=setting['port'];
		setting['pidfile']="/usr/local/redis/%s.pid"%port;
		setting['dbfilename']="%s.rdb"%port;
		config_path="./redis_conf/%s.conf"%port;
	else:
		return False,"type=key_not_found;value=port";
	ok,msg=gen_conf(config_path,setting,template);
	if not ok:
		return False,msg;
	result=os.system("redis-server %s"%config_path);
	if result==0 :
		for i in range(10):
			if ping_redis("127.0.0.1",port):
				return True,"type=ok";
			time.sleep(0.1);
	return False,"type=run_faild;value=%d"%result;

def alive_redis(request):
		result="";
		for filename in os.listdir('./redis_conf/'):
			pat=filename.split(".");
			if len(pat)==2 and pat[1]=="conf":
				port=pat[0];
				if result!="":
					result=result+":";
				ok=ping_redis("127.0.0.1",port);
				result=result+"port=%s;alive=%s"%(port,ok);
		return True,result;

def decode_command(command):
	result=[];
	commands=command.split(":");
	for i in commands:
		item={};
		fields=i.split(";");
		for f in fields:
			field=f.split("=");
			if len(field)>1:
				item[field[0]]=field[1].strip();
		result.append(item);
	return result;

def shutdown(request):
	if len(request)<2:
		return False,"type=args_not_found;value=1";
	if not "port" in request[1]:
		return False,"type=key_not_found;value=port";
	port=request[1]['port'];
	send_redis("127,0.0.1",port,"shutdown\r\n");
	for i in range(10):
		if not ping_redis("127.0.0.1",port):
			return True,"type=ok";
		time.sleep(0.1);
	return False,"type=shutdown_failed;value=unknow";


def run_command(request):
	request=decode_command(request);
	if len(request)<1:
		return False;
	if not 'command' in request[0]:
		return False,"type=key_not_found;value=command";
	cmd=request[0]['command'];
	path="";
	if cmd=="run":
		return run_redis(request);
	if cmd=="alive":
		return alive_redis(request);
	if cmd=="shutdown":
		return shutdown(request);
	if cmd=="update_template":
		return update_template(request);
	return False,"type=command_not_found;value=%s"%cmd;

def run_master(ip,port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		sock.connect((ip, int(port)));
		#sock.settimeout(2);
		buffer="";
		remain="";
		while True:
			recv=sock.recv(10240);
			request=recv.split("\n");
			if len(request)>1:
				buffer=buffer+request[0];
				remain=request[1];
			elif len(request)>0:
				buffer=buffer+request[0]
			else:
				break;
			ok,msg=run_command(buffer);
			if not ok:
				print buffer;
				print msg;
			sock.send(msg+"\n");
			buffer=remain;
			remain="";
			if not recv:
				break;
		print("connect end");
ip="127.0.0.1";
port=4999;
while True:
	try:
		run_master(ip,port);
	except socket.error,msg:
		print "connect to master:(%s %s)"%(ip,port),msg[0];
		time.sleep(1);
		continue;
#print run_command("command=shutdown:port=5001\n");
#print run_command("command=shutdown:port=5002\n");
#print run_command("command=shutdown:port=5003\n");
#print run_command("command=shutdown:port=5004\n");
#print run_command("command=alive\n");
#
#print run_command("command=run;template=default:port=5001\n");
#print run_command("command=run;template=default:port=5002\n");
#print run_command("command=run;template=default:port=5003\n");
#print run_command("command=run;template=default:port=5004\n");
#print run_command("command=alive\n");

