import atexit
import socket
import sys

from server import Server
import network

ip,port='127.0.0.1',7777

class ProxyException(Exception):
	def __init__(self,msg):
		Exception.__init__(self,msg)

class ServerProxy(object):
	'''
	fakes a connexion with a distant server.
	what's happening for real is that the server is instanciated localy, and the communication occurs on 127.0.0.1
	the goal is to be able to develop/test/play localy, while minimizing the coupling so that any further expansion of the game is eased (play on lan/online).
	'''
	def __init__(self):
		self.launch_local_server(ip,port)
		self.buf=''
		self.connect_to_server(ip,port)
		network.serverproxy=self
		out('proxy connected.')

	def connect_to_server(self,ip,port):
		try:
			self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error,e:
			raise ProxyException('local proxy could not connect to local server (socket creation error: '+str(e)+')')
		try:
			self.socket.connect((ip,port))
		except socket.error,e:
			raise ProxyException('local proxy could not connect to local server (connect error: '+str(e)+')')

	def launch_local_server(self,ip,port):
		self.server=Server(ip,port)
		if not self.server.is_open:
			raise ProxyException('local server could not get created.')

	def get_new_data(self):
		self.server.update()
		try:
			self.buf+=self.socket.recv(4096)
		except socket.error,msg:
			pass
			#print 'unable to read serverproxy\'s socket: ('+str(msg)+')'
		msg=[]
		while '\n' in self.buf:
			i=self.buf.index('\n')
			try:
				msg.append(network.packet2dict(self.buf[:i]))
			except Exception,e:
				print 'serverproxy error:',str(e)
			self.buf=self.buf[i+1:]
		return msg

	def send_config(self,conf):
		out('proxy: sending config.')
		self.send({network.cts_conf:conf})
		self.socket.setblocking(0)

	def send(self,data):
		'''
		send a dict of {meta:data,[meta:data,...]} to the server
		'''
		self.socket.send(network.dict2packet(data))

	def update(self):
		pass

	new_data=property(get_new_data)