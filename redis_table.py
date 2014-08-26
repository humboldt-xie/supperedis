
status_master="master"
status_down="down";
status_slaver="slaver";
status_newer="newer";
status_sync="sync";

hostNone="";
hostA="127.0.0.1:6379";
hostB="127.0.0.1:6378";
hostC="127.0.0.1:6377";
hostD="127.0.0.1:6377";
hostE="127.0.0.1:6377";
hostF="127.0.0.1:6377";
host="host";
status="status";
master="master";
hostlist=[
		[
			{host:hostA,status:status_master,master:hostNone},
			{host:hostB,status:status_slaver,master:hostA},
			{host:hostC,status:status_newer,master:hostB}
		],
		[
			{host:hostD,status:status_down,master:hostNone},
			{host:hostE,status:status_down,master:hostA},
			{host:hostF,status:status_newer,master:hostB}
		]
];

def get_node(hostlist,host):
	for hash in hostlist:
		for j in enumerate(hash):
			node=j[1];
			index=j[0];
			if node['host']==host:
				yield index,node,hash;
	yield None,None,None;
		
def set_down(hostlist,host):
	for index,node,hash in get_node(hostlist,host):
		if node!=None:
			node['status']=status_down;

def is_alive(node):
	if node['status']==status_master or node['status']==status_slaver :
		return True;
	return False;

def update_node(hash,copy_count,drop_down):
	#remove_down
	downlist=[];
	alive_count=0;
	for node in hash:
		if is_alive(node):
			alive_count+=1;
	if alive_count>0 or drop_down:
		flag=True;
		while flag:
			flag=False;
			index=-1;
			for n in enumerate(hash):
				if n[1]['status']==status_down:
					index=n[0];
					flag=True;
			if index>=0:
				del hash[index];
	

def update(hostlist,copy_count,drop_down):
	for hash in hostlist:
		update_node(hash,copy_count,drop_down);
	

print(hostlist);
set_down(hostlist,"127.0.0.1:6379");
print(hostlist);
update(hostlist,3,False);
print(hostlist);
