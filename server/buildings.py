
from entity import Entity,EIType
import network

class Building(Entity):
	eitype=EIType.building
	def __init__(self,*args,**kwargs):
		Entity.__init__(self)
		self.tile=kwargs['tile']
		self.owner=kwargs['owner']

class Home(Building):
	eitype=EIType.home
	def __init__(self,*args,**kwargs):
		Building.__init__(self,*args,**kwargs)
		self.owner.home=self
		for p in self.players.values():
			p.send({network.stc_new_home:{'eid':self.eid,'tileid':self.tile.eid}})#height, type etc

	def __delete__(self):
		del self.owner.home

