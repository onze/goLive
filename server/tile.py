
from panda3d.core import ConfigVariableDouble,ConfigVariableInt

from entity import Entity,EIType
import player
import network

class Tile(Entity):
	team={}
	eitype=EIType.tile
	#flag indicating to the server if the tile ratio has to be recomputed
	new_ratio=True
	#Tile.propagate_load is called every load_frame%this var
	load_propagation_frequency=ConfigVariableInt('load-propagation-frequency').getValue()
	#amount of load spread by a stone every frame
	load_amount=8.
	#amount under this threshold won't be propagated to neighbor tiles
	load_amount_threshold=.01
	max_load=255
	#load levels thresholds (numbers of frames under which the load level is at load_level_n)
	#see Tile.update_load_level
	load_level_0=ConfigVariableInt('load-level-0').getValue()
	load_level_1=ConfigVariableInt('load-level-1').getValue()
	load_level_2=ConfigVariableInt('load-level-2').getValue()
	#load can't be greater than this (allows taking back a tile quickly)
	max_load=ConfigVariableInt('load-level-2').getValue()
	#duration (in frames) during which the tile holds a stone before it disappear
	pawner_duration=ConfigVariableInt('pawner-duration').getValue()*ConfigVariableDouble('clock-frame-rate').getValue()

	def __init__(self,players,x,y,h,xres):
		self.x,self.y,self.h=x,y,h
		self.index=xres*y+x
		Entity.__init__(self)
		#defines the belonging of the tile, hence its color and how score is computed (owner property)
		#it points to a player (its pid)
		self.owner=None
		#pid of the owner of the unit that drops a stone on the tile
		self._pawner=None
		#load units counter, used to determine the load level
		self.load=0
		#level at which the tile belongs to its owner. see Tile.update_load_level for details.
		self.load_level=0
		#records the number of frames since last pawner change
		self.load_frames=-1
		#il == instant load.
		#inter frame load, per source tile.owner.pid
		self.il={}
		#inter frame load source tile, per source tile.owner.pid
		self.il_src={}
		self.reset_il()
		#see Tile.pawner_duration
		self.pawner_duration=Tile.pawner_duration
		for p in self.players.values():
			p.send({network.stc_new_tile:{'eid':self.eid,'x':x,'y':y}})#height, type etc

	def add_load(self,src,pid,load):
		self.il[pid]+=load
		if not src in self.il_src and src!=self:
			self.il_src[pid].append(src)
		if not self.resolve_load in self.server.eof_list:
			self.server.eof_list.append(self.resolve_load)

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
			
	def get_pawner(self):
		'''property getter'''
		return self._pawner
	
	def get_right_tile(self):
		'''property getter'''
		if self.x<self.server.xres-1:return Entity.instances[self.eitype][self.index+1]
		return None 

	def get_team(self):
		'''property'''
		return self._team
	
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
			
	def propagate_load(self):
		self.load_frames+=1
		if self.load_frames%Tile.load_propagation_frequency==0:
			self.add_load(self,self._pawner.pid,Tile.load_amount)
		if self.load_frames==self.pawner_duration:
			self.pawner=None
			self.server.update_list.remove(self.propagate_load)

	def reset_il(self):
		for pid in player.Player.instances:
			self.il[pid]=0
			self.il_src[pid]=[]

	def resolve_load(self):
		for pid in self.il:
			iload=self.il[pid]
			if iload==0:
				continue
			if self.owner==None:
				self.owner=pid
			if pid==self.owner:
				self.load+=iload
			else:
				self.load-=iload
				if self.load<=0:
					self.load=0
					self.owner=pid
		load=max([self.il[pid] for pid in self.il])
		self.update_load_level()
		#propagate
		if self.load_level>1:
			nei=[]
			for n in self.neighbors:
				if n._pawner!=None:continue
				if n._pawner==self._pawner and self._pawner!=None:continue
				if n in self.il_src[self.owner]:continue
				nei.append(n)
			if len(nei):
				#propagated_load=load/float(len(nei))
				propagated_load=load/4.
				if propagated_load>Tile.load_amount_threshold:
					[n.add_load(self,self.owner,propagated_load) for n in nei]
		#clear instant load
		self.reset_il()
	
	def set_pawner(self,p):
		'''property'''
		if self._pawner!=p:
			self._pawner=p
			self.load_frames=-1
			if p!=None:
				if not self.propagate_load in self.server.update_list: 
					self.server.update_list.append(self.propagate_load)
				self.bufferize({network.stc_tile_change_pawner:{'eid':self.eid,'pawner':self._pawner.pid}})
			else:
				if self.propagate_load in update_list:
					update_list.remove(self.propagate_load)
				self.bufferize({network.stc_tile_change_pawner:{'eid':self.eid,'pawner':None}})

	def set_eitype(self,t=None):
		Entity.instances[self.eitype][self.index]=self

	def set_team(self,t):
		'''property'''
		self._team=t

	def update_load_level(self):
		'''
		sets up self.load_level according to self.load.
		levels are:
		#0: tile's just been marked (could still be easily taken back by another player, so wait and see),
		#1: tile has been 'secured' enough by a player to update it client side,
		#2: tile is loaded enough to propagate its load to neighbors,
		#3: tile is fully loaded.
		'''
#		out(lvl0=Tile.load_level_0,lvl1=Tile.load_level_1,lvl2=Tile.load_level_2)
		#load level
		save=self.load_level
		if self.load<Tile.load_level_0:
			self.load_level=0
		elif self.load<Tile.load_level_1:
			self.load_level=1
		elif self.load<Tile.load_level_2:
			self.load_level=2
		else:
			self.load_level=3
			self.load=Tile.max_load
		#update client if level has changed (level 2 is internal)
		if self.load_level!=save and self.load_level!=2:
			self.bufferize({network.stc_tile_load_level_change:{'eid':self.eid,'owner':self.owner,'level':self.load_level}})

	pawner=property(get_pawner,set_pawner)
	team=property(get_team,set_team)
	upper_tile=property(get_upper_tile)
	left_tile=property(get_left_tile)
	lower_tile=property(get_lower_tile)
	right_tile=property(get_right_tile)
	neighbors=property(get_neighbors)
