
from math import atan2,cos,sin

from entity import Entity,EIType
from tile import Tile
from tools import dist2
import network

class Unit(Entity):
	eitype=EIType.unit
	def __init__(self,player):
		Entity.__init__(self)
		self.owner=player
		self.tile=self.owner.home.tile
		self.send(self.confirmation_msg)
		#data related to moves
		'''list of Tiles to pass by. see update_path_following for details.'''
		self.move_path=[]
		self.x,self.y=self.tile.x,self.tile.y
		self.move_speed=.05
	
	@property
	def confirmation_message(self):
		raise Exception('Abstract unitinstanciation !')
	
	def add_to_path(self,tile):
		'''
		adds a tile to the path. the unit will start goinf to this tile ass soon as 
		it becomes the next destination to go to.
		'''
		self.move_path.append(tile)
		#first move in the list: client must be warned
		if len(self.move_path)==1:
			d=dist2(self,self.move_path[0])
			self.d=d
			self.send({network.stc_unit_moving:{'eid':self.eid,
											    'start':self.tile.eid,
											    'end':self.move_path[0].eid,
											    'begin':self.frame_no,
											    'frames':d/self.move_speed
											    }})
			self.server.update_list.append(self.update_path_following)
		
	def update_path_following(self):
		'''
		if self.path is not empty, the unit will move at its self.speed from its current position towards
		the first element in self.path.
		'''
		if len(self.move_path)==0:return
		#not arrived yet
		d=dist2(self,self.move_path[0])
#		out('server '+str((self.d-d)*100./self.d))
		if d>self.move_speed:
			ox,oy=self.x,self.y
			#move (angle could be cached)
			a=atan2(self.move_path[0].y-self.y,self.move_path[0].x-self.x)
			self.x+=self.move_speed*cos(a)
			self.y+=self.move_speed*sin(a)
			#unit may have moved to a new tile
			if int(ox)!=int(self.x) or int(oy)!=int(self.y):
				self.tile=self.get_tile(self.x,self.y)
#				self.send({stc_unit_tile:{'eid':self.eid,'tile':self.tile.eid}})
		else:
			#arrived
			out('server side:arrived')
			self.tile=self.move_path.pop(0)
			self.x,self.y=self.tile.x,self.tile.y
			self.send({network.stc_unit_move_over:{'eid':self.eid,'tile':self.tile.eid}})
			if len(self.move_path)>0:
				d=dist2(self,self.move_path[0])
				self.send({network.stc_unit_moving:{'eid':self.eid,
												    'start':self.tile.eid,
												    'end':self.move_path[0].eid,
												    'begin':self.frame_no,
												    'frames':d/self.move_speed
												    }})
			else:
				self.server.update_list.remove(self.update_path_following)

	   
	