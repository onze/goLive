
import atexit
import select
import socket
import sys

from direct.fsm import FSM
from panda3d.core import ConfigVariableInt

from ai import AI
from buildings import Home
import default
from entity import Entity,EIType
from node import Node
from player import Player
from tile import Tile
from tilerationotifier import TileRatioNotifier
import network

class Server(FSM.FSM,Node):
	def __init__(self,ip,port):
		FSM.FSM.__init__(self, 'Server.fsm')
		self.defaultTransitions = {
			'Accepting':['Conf'],
			'Conf':['Running'],
			'Running':['Closing'],
			'Closing':[]
			}
		atexit.register(self.close)
		try:
			self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			Node.__init__(self,self.socket)
		except socket.error,msg:
			print 'local server could not get ready (socket creation error:',msg,')'
			self.close()
			sys.exit()
		try:
			self.socket.bind((ip,port))
		except socket.error,msg:
			print 'local server could not get ready (bind error:',msg,')'
			self.close()
			sys.exit()
		self.socket.listen(1)
		self.is_open=True
		'''incoming data (as strings, but still) buffer'''
		self.buf=''
		'''methods appended in this list are called once a frame, until they are removed from it
		the calls don't happen before the 'Running' state'''
		self.update_list=[]
		'''methods appended in this list are called at the end of the current frame,
		and then removed from it automatically. this list is double buffered, 
		so that anything added to it during its processing will be called at the end of the next frame.''' 
#		self.eof_list=[]
		'''dict of players (by id)'''
		self.players={}
		Entity.players=self.players
		Entity.server=self
		print 'local server open on ',ip,':',port
		'''for synchronization purposes:
		to each event sent to a client is attached the frame number.
		this works as a marker of time'''
		self.frame_no=Player.frame_no=Entity.frame_no=0
		'''objects that want to be removed add themselves to this list
		it is then sure they'll be deleted 'from outside'''
		self.del_list=[]
		self.demand('Accepting')

	def close(self):
		self.socket.close()
		print 'server closed.'

	def dummy(self):
		'''default dummy update.does nothing.'''
		pass

	def enterAccepting(self):
		print 'server::enterAccepting'
		self.socket.setblocking(0)
		Server.update=Server.update_accept

	def exitAccepting(self):
		Server.update=Server.dummy

	def enterConf(self):
		Server.update=Server.update_conf

	def exitConf(self):
		Server.update=Server.dummy

	def enterRunning(self):
		self.frame_no=0
		self.tile_ratio_notifier=TileRatioNotifier(self)
		Server.update=Server.update_running

	def exitRunning(self):
		Server.update=Server.dummy

	def enterClosing(self):pass
	def exitClosing(self):pass

	def filter_conf(self,pconf):
		'''
		check the received conf validity
		'''
		warning_intro='WARNING in Server.filter_conf: '
		#check that all tags are present
		for tag in ['cpu','map.res']:
			if not tag in pconf:
				out(warning_intro+'missing \''+tag+'\' tag. default value will be used')
				pconf[tag]=default.game_conf[tag]
		sconf={}
		#build the conf from tags, checking their validity beforehands
		if not (pconf['cpu']==True or pconf['cpu']==False):
			out(warning_intro+'invalid \'cpu\' tag. default value will be used')
			pconf['cpu']=default.game_conf['cpu']
		sconf['cpu']=pconf['cpu']
		if not pconf['map.res'] in ['xs','s','m','l']:
			out(warning_intro+'invalid \'map.res\' tag. default value will be used')
			pconf['map.res']=default.game_conf['map.res']
		sconf['map.res']=pconf['map.res']
		return sconf

	def read(self):
		'''
		generator of received messages.
		must be read until exhaustion before being able to read new messages.
		'''
		for p in self.players.values():
			for msg in p.read():
				yield msg

	def send(self,d):
		'''
		sends a dict {network.code:value} to all players
		'''
		for p in self.players.values():
			p.send(d)

	def send_string(self,d):
		'''
		sends a string (as given) to all players
		'''
		for p in self.players.values():
			p.send_string(d)

	def set_conf(self,conf):
		'''processes the conf sent by the player.'''
		#instanciates an ai (or later takes a player's socket)
		if conf['cpu']:
			ai=AI(AI.next_pid())
			self.players[ai.pid]=ai
		#build the map
		xres=ConfigVariableInt('map-width-'+conf['map.res']).getValue()
		yres=ConfigVariableInt('map-height-'+conf['map.res']).getValue()
		Entity.instances[EIType.tile]=[None]*(xres*yres)
		for x in range(xres):
			for y in range(yres):
				Tile(self.players,x,y,0,xres)
		self.xres,self.yres=xres,yres
		if None in Entity.instances[EIType.tile]:
			raise Exception('in Server.set_conf: holes in Entity.instances[EIType.tile]. all tiles must be initialised.')
		print xres/2
		print len(Entity.instances[EIType.tile])
		Home(tile=Entity.instances[EIType.tile][xres/2],owner=self.players[0])
		Home(tile=Entity.instances[EIType.tile][(yres-1)*xres+xres/2],owner=self.players[1])

	def update_accept(self):
		print 'SERVER::update_accept()'
		read,_,_=select.select([self.socket],[],[],0)
		if len(read)>0:
			socket,address=self.socket.accept()
			print 'got player @',address
			p=Player(socket,address,Player.next_pid(),self)
			self.players[p.pid]=p
			self.demand('Conf')

	def update_conf(self):
		'''
		receives the conf and sets itself up according to it,
		then sends a first batch of setup (although regular) instructions to clients.
		'''
		for d in self.read():
			print 'SERVER::received:',d
			if network.cts_conf in d:
				conf=self.filter_conf(d[network.cts_conf])
				self.send({network.stc_conf:conf})
				self.set_conf(conf)
				self.send({network.stc_start_game:''})
				self.demand('Running')

	def update_running(self):
#		out('server update',frame_no=self.frame_no)
		Node.frame_no=self.frame_no=self.frame_no+1
		
		[f() for f in self.update_list]
		
#		temp=self.eof_list
#		self.eof_list=[]
#		[f() for f in temp]
		
		self.tile_ratio_notifier.update()
		
		for o in self.del_list:del o
		self.del_list=[]
		
		self.flush_buffer()
			

