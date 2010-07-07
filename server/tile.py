
from entity import Entity,EIType
import network

class Tile(Entity):
	team={}
	eitype=EIType.tile
	def __init__(self,players,x,y,h,xres):
		self.x,self.y,self.h=x,y,h
		self.index=xres*y+x
		Entity.__init__(self)
		#defines the belonging of the tile, hence its color and how score is computed (owner property)
		#it points to a player
		self.current_owner=None
		for p in self.players.values():
			p.send({network.stc_new_tile:{'eid':self.eid,'x':x,'y':y}})#height, type etc
			
	def get_owner(self):
		'''property'''
		return self.current_owner
	
	def get_left_tile(self):
		if self.x>0:return Entity.instances[self.eitype][self.index-1]
		return None
	
	def get_lower_tile(self):
		if self.y>0:return Entity.instances[self.eitype][self.index-self.server.yres]
		return None
	
	def get_right_tile(self):
		if self.x<self.server.xres-1:return Entity.instances[self.eitype][self.index+1]
		return None 
	
	def get_upper_tile(self):
		if self.y<self.server.yres-1:return Entity.instances[self.eitype][self.index+self.server.yres]
		return None
	
	def get_neighbors(self):
		return filter(lambda t:t!=None,
					  [self.get_left_tile(),
					   self.get_lower_tile(),
					   self.get_right_tile(),
					   self.get_upper_tile()])

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
		while len(fringe)>0:
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
	
	def set_owner(self,o):
		'''property'''
		if self.current_owner!=o:
			self.current_owner=o
			for p in self.players.values():
				p.send({network.stc_tile_owner_change:{'eid':self.eid,'owner':self.current_owner.pid}})

	def distance_to(self,target):
		return (target.x-self.x)+(target.y-self.y)

	def get_team(self):
		'''property'''
		return self._team

	def set_eitype(self,t=None):
		Entity.instances[self.eitype][self.index]=self

	def set_team(self,t):
		'''property'''
		self._team=t

	owner=property(get_owner,set_owner)
	team=property(get_team,set_team)
	upper_tile=property(get_upper_tile)
	left_tile=property(get_left_tile)
	lower_tile=property(get_lower_tile)
	right_tile=property(get_right_tile)
	neighbors=property(get_neighbors)
