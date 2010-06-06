
from entity import Entity,EIType
import network

class Tile(Entity):
	team={}
	eitype=EIType.tile
	def __init__(self,players,x,y,h,xres):
		self.x,self.y,self.h=x,y,h
		self.index=xres*y+x
		Entity.__init__(self)
		for p in self.players.values():
			p.send({network.stc_tile_sync:{'eid':self.eid,'x':x,'y':y}})#height, type etc
			
	def distance_to(self,target):
		return (target.x-self.x)+(target.y-self.y)

	def get_team(self):
		return self._team

	def set_eitype(self,t=None):
		Entity.instances[self.eitype][self.index]=self

	def set_team(self,t):
		self._team=t

	team=property(get_team,set_team)
