高可用性，分片，牺牲部分同步性,
要求： 自组织，无人工配置。 人申请资源为-名称-资源-类型-策略,所有需要配置的，只是master程序，所有worker程序只需要连上master即可。
思路
	分两个程序 
	worker  修改配置 负责启动redis 关闭redis  检测redis是否 还活着
	master  负责对业务管理配置，分配redis  [host1,host2,...]-[index1,index2] host1 为主 host2 和后面的为从

	host={
		alive:
		memory:
		cpu:
		readonly:
		bussiness:
		index:[]
	}
	检测host1 挂掉，则切换master到host2,然后报给各个客户端

	分裂策略-当内存达到最大80%，且非纯内存cache
	分裂流程:
		index[1,2,3,4] 分裂成2个redis为: index1[1,2] index[3,4]
		新开一个redis，创建 两个slave 并等待slave 同步完成
		此时状态:master slaveA  slaveB
			设置slaveA slaveB为可读
		配置文件为[ {host=[master:rw,slaveA:rw],index=[1,2] }
					{host=[master:rw,slaveB:rw],index=[3,4] }
				  ]
		待所有客户端配置更新完毕，则杀死master，那么，使用者即可自动读写slaveA 或slaveB
		slaveA slaveB断开主从

	新版旧版更新问题：

	可扩展，但不可收缩.. ..

	客户端程序在发现错误时，主动向master 获取新redis 列表
	每个redis 启动后，都有一个配置版本

	可能出现的问题  
			主挂掉，后不可写  直到从升为主   
			开的实例过多，影响性能


	协议修改为  index:key  index 为哈希 同一index肯定是落在同一个redis的。 修改客户端，自动转换两者关系。 而由使用者根据具体情况，算出index。



配置算法问题：
	有N个桶，分配给C*H个服务，且如果同个桶有C台服务都挂掉，服务有两种策略，一种是重新分配服务，一种是设置为不可用，并报警
	当主的挂掉，备用的变主,当备用的挂掉，重新分配一台。

