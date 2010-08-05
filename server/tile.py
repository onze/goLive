
#from panda3d.core import ConfigVariableDouble,ConfigVariableInt

from entity import Entity,EIType
#import player
import network

class Tile(Entity):
	team={}
	eitype=EIType.tile
	'''flag indicating to the server if the tile ratio has to be recomputed'''
	new_ratio=True
	'''updated by tiles on owner change, to keeps ratio in sync'''
	ratio={}

	def __init__(self,players,x,y,h,xres):
		self.x,self.y,self.h=x,y,h
		self.index=xres*y+x
		Entity.__init__(self)
		#defines the belonging of the tile, hence its color and how score is computed (owner property)
		#it points to a player (its pid)
		self._owner=None
		#pid of the owner of the unit that drops a stone on the tile
		self._pawner=None
		self.send({network.stc_new_tile:{'eid':self.eid,'x':x,'y':y}})#height, type etc

	def distance_to(self,target):
		return (target.x-self.x)+(target.y-self.y)
	
	def get_left_tile(self):
		'''property getter'''
		if self.x>0:return Entity.instances[self.eitype][self.index-1]
		return None
	
	def get_lower_tile(self):
		'''property getter'''
		if self.y>0:return Entity.instances[self.eitype][self.index-self.server.yres]
		return None
	
	def get_neighbors(self):
		'''property getter'''
		return filter(lambda t:t!=None,
					  [self.get_left_tile(),
					   self.get_lower_tile(),
					   self.get_right_tile(),
					   self.get_upper_tile()])
	
	def get_owner(self):
		'''property getter'''
		return self._owner
			
	def get_pawner(self):
		'''property getter'''
		return self._pawner
	
	def get_right_tile(self):
		'''property getter'''
		if self.x<self.server.xres-1:return Entity.instances[self.eitype][self.index+1]
		return None
	
	def get_upper_tile(self):
		'''property getter'''
		if self.y<self.server.yres-1:return Entity.instances[self.eitype][self.index+self.server.yres]
		return None

	def path_to(self,dst,player=None):
		'''
		returns a list of tiles to go from this tile to dst tiles.
		this tile is not included, dst is.
		args:
		-dst: the destination tile
		kwargs (filters):
		-player: ignore tiles marked as belonging to other players (different pid).
		'''
		#TODO: implement filters
		#non recursive breadth first dijkstra search
		fringe=[self]
		#{tile:(prev,dist)}
		dijkstra={self:[None,0]}
		while len(fringe):
			t=fringe.pop(0)
			if t==dst:break
			for neighbor in t.neighbors:
				dist=dijkstra[t][1]+1
				if (not neighbor in dijkstra) or (dijkstra[neighbor][1]>dist):
					dijkstra[neighbor]=[t,dist]
					if not neighbor in fringe:
						fringe.append(neighbor)
		path=[]
		while t!=self:
			path.insert(0,t)
			t=dijkstra[t][0]
		#out('Tile.path_to: path='+str(map(str,[t.eid for t in path])))
		return path
	
	def set_pawner(self,p):
		'''property'''
		if self._pawner!=p:
			self._pawner=p
			if p!=None:
				self.bufferize({network.stc_tile_change_pawner:{'eid':self.eid,'pawner':self._pawner.pid}})
			else:
				self.bufferize({network.stc_tile_change_pawner:{'eid':self.eid,'pawner':None}})

	def set_eitype(self,t=None):
		'''property setter'''
		Entity.instances[self.eitype][self.index]=self
		
	def set_owner(self,o):
		'''property setter'''
		Tile.ratio_notifier.update_ratio(self._owner,o)
		self._owner=o

	pawner=property(get_pawner,set_pawner)
	upper_tile=property(get_upper_tile)
	left_tile=property(get_left_tile)
	lower_tile=property(get_lower_tile)
	right_tile=property(get_right_tile)
	neighbors=property(get_neighbors)
	owner=property(get_owner,set_owner)
