
import network
import socket
import sys

from sprinter import HSprinter,VSprinter

class Player:
	#each player has an id that comes from here.
	next_pid=(i for i in xrange(sys.maxint)).next
	#player (including ia) instances, by pid
	instances={}
	def __init__(self,socket,address,pid,server):
		self.pid=pid
		Player.instances[self.pid]=self
		self.socket=socket
		self.socket.setblocking(0)
		self.address=address
		self.buf=''
		self.server=server
		self.server.update_list.append(self.update)
		#sum of tiles under player control
		self.owned_tiles=0
		
	def dispose(self):
		'''del'''
		del Player.instances[self.pid]
		self.server.update_list.remove(self.update)

	def new_unit(self,conf):
		'''
		called when a client request a new unit.
		checks conf validity and instanciates the unit if allowed.
		also convert properties types to what is expected.
		'''
		error_intro='ERROR in Player.new_unit(conf='+str(conf)+':'
		if conf['unit_type']=='v_sprinter' or conf['unit_type']=='h_sprinter':
			valid=True
			try:
				conf['x']=int(conf['x'])
			except:
				out(error_intro+' int can\'t parse conf[\'x\'])')
				valid=False
			if not -1<conf['x']<self.server.xres:
				out(error_intro+' conf is not valid: -1<conf[\'x\']='+str(conf['x'])+'<self.server.xres='+str(self.server.xres)+'')
				valid=False
			try:
				conf['y']=int(conf['y'])
			except:
				out(error_intro+' int can\'t parse conf[\'y\'])')
				valid=False 
			if not -1<conf['y']<self.server.yres:
				out(error_intro+' conf is not valid: -1<conf[\'y\']='+str(conf['y'])+'<self.server.yres='+str(self.server.yres)+'')
				valid=False
			if valid:
				if conf['unit_type']=='v_sprinter':
					VSprinter(self,conf)
				elif conf['unit_type']=='h_sprinter':
					HSprinter(self,conf)				

	def receive(self):
		complete_msg=[]
		try:
			self.buf+=self.socket.recv(4096)
		except socket.error,msg:
			#nothing to read
#			print 'unable to read player\'s (pid='+str(self.pid)+') socket: ('+str(msg)+')'
			pass
		while '\n' in self.buf:
			i=self.buf.index('\n')
			try:
				complete_msg.append(network.packet2dict(self.buf[:i]))
			except Exception,e:
				out('ERROR in Player(pid='+str(self.pid)+').receive: '+str(e)+'. skipped.')
			self.buf=self.buf[i+1:]
		return complete_msg
		

	def send(self,d):
		'''
		d is a dict {meta:values}
		'''
		d['frame_no']=self.frame_no
		self.socket.send(network.dict2packet(d))

	def update(self):
		switch={  network.cts_new_unit:self.new_unit
			    }
		for pkt in self.receive():
			#pkt is a dict
			for key in pkt.keys():
				if key in switch:
					out('server.player: processing pkt['+str(key)+']='+str(pkt[key]))
					switch[key](pkt[key])
				else:
					out('ERROR unknown pkt:'+str(pkt)+'. skipping.')
