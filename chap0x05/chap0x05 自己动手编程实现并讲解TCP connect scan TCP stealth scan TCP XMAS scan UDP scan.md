# chap0x05 自己动手编程实现并讲解TCP connect scan/TCP stealth scan/TCP XMAS scan/UDP scan

----------

## 实验要求
* 自己动手编程实现并讲解TCP connect scan/TCP stealth scan/TCP XMAS scan/UDP scan
## 实验环境
* 客户端
	<pre>
	名称：Client
	网卡：eth0
	IP：10.0.2.5
	</pre>
* 服务端
	<pre>
	名称：Server
	网卡：eth1
	IP：10.0.2.8
	</pre>
## 实验过程
### 实验开始前
* 已知主机状态分为
	* 可达（在线），则端口状态分为
		* 开放：有条件有规则地响应请求数据报文
		* 关闭：有条件有规则地响应或忽略请求数据报文
		* 被过滤：有条件有规则地响应或忽略请求数据报文
	* 不可达（离线）
		* 无开放端口，对任何类型的请求数据包均无响应
* 本此实验涉及上述三种端口状态：开放，关闭，不可达(指主机)
* Server端开放TCP端口方式`root@Server:~# python2 -m SimpleHTTPServer 80`
* Server端开放UDP端口方式
	<pre>
	import socket
	addr="10.0.2.8"
	port=8080
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((addr, port))
	print("waiting for message...")
	while True:
	    data,address=s.recvfrom(1024)
	    s.sendto('',address)
	</pre>
* Server端抓包指令`tcpdump -n -i eth1 host 10.0.2.5 and port not 22`
	* server端的22端口已与Client建立ssh连接，需过滤掉
### TCP connect scan
* ![](image\TCP_connect_scan_open.png)
* 过程
	* `root@Server:~# python2 main.py <type> <address> <port> <flags>`
	![](image\tcp_connect_scan.png)
* 分析：
	* 当Client要与Server端**开放**的TCP端口建立连接：
		1. Client会先发送flags字段为`S`(0x02)的数据包
		2. Server收到后从80端口返回flags字段为`SA`(0x12)的数据包
		3. Client收到后再返回flags字段为`AR`(0x14)的数据包，至此连接建立
		* 上述第二步时Client自动回复了一个flags字段为`R`的数据包，通过参考同学的作业明白该数据包是操作系统自己回复的。由于操作系统没有监听我们发第一次握手包时的端口，所以对于外部来的`SA`，操作系统自然会回复`R`。
	* 当Client要与Server端**未开放**的TCP端口建立连接：
		1. Client会先发送flags字段为`S`(0x02)的数据包
		2. Server收到后从该端口(实验中为808端口)返回flags字段为`RA`的数据包表示端口处于关闭状态。
	* 当Client要与**离线**状态的Server端建立TCP连接
		* Client发送flags字段为`S`(0x02)的数据包后未收到回复，表示主机不可达。
### TCP stealth scan
* ![](image\TCP_stealth_scan.png)
* 过程
	![](image\tcp_stealth_scan_pro.png)
* 分析：tcp stealth scan与TCP connect scan连接扫描相似，只是在第三次握手时Client只返回flags字段为`R`的数据包，然后连接建立完成。
### TCP XMAS scan
* ![](image\TCP_XMAS_scan.png)
* 过程
	![](image\TCP_XMAS_scan_pro.png)
* 分析
	* 当Client要与Server端**开放**的TCP端口建立连接
		* Client会先发送flags字段为`FPU`的数据包，如果端口是开放的，则Client不会收到任何回复
	* 当Client要与Server端**未开放**的TCP端口建立连接：
		* Client先发送flags字段为`FPU`的数据包
		* Server收到后从该端口(实验中为808端口)返回flags字段为`RA`的数据包表示端口处于关闭状态。
### UDP scan
* ![](image\udp_scan.png)
* 过程
	![](image\udp_scan_pro.png)
* 分析
	* UDP是无连接的协议,通信双方无需建立通信信道，只要Client到Server存在可用信道。
	* 当Client要与Server端**开放**的UDP端口建立连接
		* Client向Server的8080端口发送UDP数据包
		* Server收到后向Client回复**UDP**包，则Client收到回复后认为目标端口是可通信的。
	* 当Client要与Server端**未开放**的UDP端口建立连接：
		* Client向Server的808端口发送UDP数据包
		* Server收到后从该端口(实验中为808端口)回复一个**ICMP**包，并说明Server的目标udp端口不可达。
### 结尾
* 参考资料[http://resources.infosecinstitute.com](http://resources.infosecinstitute.com/port-scanning-using-scapy/)
* 参考同学作业[https://github.com/CUCCS/2018-NS-Public-TheMasterOfMagic](https://github.com/CUCCS/2018-NS-Public-TheMasterOfMagic/tree/ns-chap0x05)