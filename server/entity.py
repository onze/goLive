
import sys

'''the entity instance type allows easy differenciation/selection between entities.'''
class EIType:
	entity='entity'
	tile='tile'
	building='building'
	home='home'
	unit='unit'

class Entity(object):
	'''an Entity is anything that lives both server side and client side'''
	'''each entity has an id that comes from here.'''
	next_eid=(i for i in xrange(sys.maxint)).next
	'''dict of {entity instance type:list of entities}.
	- instances['EIType.tile']: tiles' coordinates are converted to indexes (setup in Server.set_conf)'''
	instances={}
	'''default entity type'''
	eitype=EIType.entity

	def __init__(self):
		self.eid=self.next_eid()
		self.set_eitype(self.eitype)
		
	def dispose(self):
		print 'Entity.__del__()'
		self.unset_eitype()

	def bufferize(self,d):
		'''same as server.bufferize(d)
		sends to all players.'''
		self.server.bufferize(d)
		
	def find_tile(self,x,y):
		x,y=int(x),int(y)
		return [tile for tile in self.instances[EIType.tile] if tile.x==x and tile.y==y][0]

	def max_x_for_y_tile(self,y):
		'''
		returns the tile that has the maximum x and the given y.
		'''
		return max([(tile.x,tile) for tile in self.instances[EIType.tile] if tile.y==y])[1]

	def min_x_for_y_tile(self,y):
		'''
		returns the tile that has the minimum x and the given y.
		'''
		return min([(tile.x,tile) for tile in self.instances[EIType.tile] if tile.y==y])[1]

	def max_y_for_x_tile(self,x):
		'''
		returns the tile that has the maximum x and the given y.
		'''
		return max([(tile.y,tile) for tile in self.instances[EIType.tile] if tile.x==x])[1]

	def min_y_for_x_tile(self,x):
		'''
		returns the tile that has the minimum x and the given y.
		'''
		return min([(tile.y,tile) for tile in self.instances[EIType.tile] if tile.x==x])[1]

	def send(self,d):
		'''same as server.send(d)
		sends to all players.'''
		self.server.send(d)

	def set_eitype(self,t=None):
		if t==None:
			print 'WARNING in Entity.set_eitype(): eitype not defined for class %s'%str(self.__class__)
			return
		if not Entity.instances.has_key(t):
			Entity.instances[t]={}
		Entity.instances[t][self.eid]=self
		
	
	def unset_eitype(self):
		'''used at entity removal, to clear links to it'''
		del Entity.instances[self.eitype][self.eid]
