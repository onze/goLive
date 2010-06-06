
from entity import EIType
from unit import Unit
import network

class Sprinter(Unit):
	'''abstract class to factorize sprinter behavior'''
	def __init__(self,player,conf):
		Unit.__init__(self,player)
		self.build_path_to_defined_line(conf)
		
class HSprinter(Sprinter):
	def __init__(self,player,conf):
		Sprinter.__init__(self,player,conf)
		
	@property
	def confirmation_msg(self):
		return {network.stc_new_unit:{'pid':self.owner.pid,'eid':self.eid,'type':'h_sprinter','tileid':self.tile.eid}}
	
	def build_path_to_defined_line(self,conf):
		#choose right or left side
		if conf['x']>self.tile.x:
			first=self.max_x_for_y_tile(self.tile.y)
		else:
			first=self.min_x_for_y_tile(self.tile.y)
		self.add_to_path(first)
		#climb to right height
		join=self.get_tile(x=first.x,y=conf['y'])
		self.add_to_path(join)
		#then go to the other side
		if conf['x']>self.tile.x:
			last=self.min_x_for_y_tile(join.y)
		else:
			last=self.max_x_for_y_tile(join.y)
		self.add_to_path(last)
	

class VSprinter(Sprinter):
	def __init__(self,player,conf):
		Sprinter.__init__(self,player,conf)
		
	@property
	def confirmation_msg(self):
		return {network.stc_new_unit:{'pid':self.owner.pid,'eid':self.eid,'type':'v_sprinter','tileid':self.tile.eid}}
	
	def build_path_to_defined_line(self,conf):
		#choose right or left side
		first=self.min_y_for_x_tile(conf['x'])
		self.add_to_path(first)
		
		last=self.max_y_for_x_tile(conf['x'])
		self.add_to_path(last)

