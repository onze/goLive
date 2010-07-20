
from math import atan2,cos,sin
import sys

from entity import Entity,EIType
from tile import Tile
from tools import dist2
import network

class Unit(Entity):
	eitype=EIType.unit
	def __init__(self,player):
		Entity.__init__(self)
		self.owner=player
		self.current_tile=self.owner.home.tile
		#player the unit belongs to. can be none if the unit is neutral
		#data related to moves
		'''list of Tiles to pass by (every tiles). see update_path_following for details.'''
		self.path=[]
		'''list of target tiles (does't change until next target is reached)'''
		self.target_path=[]
		'''index of next tile within tile_path'''
		#self.path_index=0
		self.x,self.y=self.tile.x,self.tile.y
		self.move_speed=.05
		#when set to true, the unit will mark tiles on its way
		self.is_marking=False
		self.send(self.confirmation_msg)
		
	def __del__(self):
		Entity.__del__(self)
		print 'Unit.__del__()'
		self.owner=None
		self.tile=None
		self.path=[]
		self.target_path=[]
	
	def add_to_path(self,tile):
		'''
		adds a tile to the target path. the unit will start going to this tile as soon as 
		it becomes the next target to go to.
		'''
		self.target_path.append(tile)
		#first move in the list: client must be warned, and move update triggered
		if len(self.target_path)==1:
			self.path=self.current_tile.path_to(self.target_path[0],player=self.owner)
			self.send({network.stc_unit_add_path:{'eid':self.eid,
												  'path':[tile.eid for tile in self.path]}})
			if not self.update_path_following in self.server.update_list: 
				self.server.update_list.append(self.update_path_following)

	def get_confirmation_msg(self):
		'''property'''
		raise Exception('Abstract unit instanciation !')
	
	def get_tile(self):
		'''property'''
		return self.current_tile
	
	def move_over(self):
		'''
		called when the unit has finished moving and need to be removed.
		'''
		self.send({network.stc_unit_move_over:{'eid':self.eid,'tile':self.tile.eid}})
		self.server.del_list.append(self)
		
	def on_tile_change(self):
		'''event handler called when the unit's tile changes.'''
		pass
	
	def set_tile(self,t):
		'''property'''
		if self.current_tile!=t:
			self.current_tile=t
			if t==None:
				return
			self.on_tile_change()
		
	def start_marking(self):
		self.is_marking=True
		
	def stop_marking(self):
		self.is_marking=False
		
	def tile_path(self,src,dst):
		'''
		returns a list of tiles to go from src to dst tiles (src and dst are not included)
		'''
		return self.current_tile.path_to(src=src,dst=dst,player=self.owner)
	
	def update_path_following(self):
		'''
		if self.path is not empty, the unit moves at its self.move_speed 
		from its current position towards the first element in self.path.
		'''
		#should have been removed before
		if len(self.path)==0:
			out('WARNING in Unit.update_path_following: self.path==0, but method still in update_list.')
			self.server.update_list.remove(self.update_path_following)
			return
		d=dist2(self,self.path[0])
		#not arrived yet
		if d>self.move_speed:
			oldx,oldy=self.x,self.y
			#move (angle could be cached at next-tile-choice)
			a=atan2(self.path[0].y-self.y,self.path[0].x-self.x)
			self.x+=self.move_speed*cos(a)
			self.y+=self.move_speed*sin(a)
			#unit has moved to a new tile
			if int(oldx)!=int(self.x) or int(oldy)!=int(self.y):
				self.tile=self.find_tile(x=self.x,y=self.y)
				#self.send({stc_unit_tile:{'eid':self.eid,'tile':self.tile.eid}})
		else:
			#arrived at path[0]
			self.tile=self.path.pop(0)
			self.x,self.y=self.tile.x,self.tile.y
			#out('server '+str(self.tile.eid))
			#path has ran out of tiles
			if len(self.path)==0:
				#should be the same
				if not self.tile==self.target_path[0]:
					out('ERROR in Unit.update_path_following: path does\'nt end on target. aborting move.')
					#self.send({network.stc_unit_abort_move:{'eid':self.eid}})
					return
				self.target_path.pop(0)
				#still has targets to reach
				if len(self.target_path)>0:
					self.path=self.current_tile.path_to(self.target_path[0],player=self.owner)
					self.send({network.stc_unit_add_path:{'eid':self.eid,
														  'path':[tile.eid for tile in self.path]}})
				else:
					#move over
					self.move_over()
					self.server.update_list.remove(self.update_path_following)
	
	confirmation_msg=property(get_confirmation_msg)
	tile=property(get_tile,set_tile)
	   
	