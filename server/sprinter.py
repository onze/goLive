
from tilemarker import TileMarker
import network

class Sprinter(TileMarker):
	'''abstract class to factorize sprinter behavior'''
	def __init__(self,player,conf):
		TileMarker.__init__(self,player)
		#set the main tiles to pass by
		first=self.find_first_target_tile(conf['x'],conf['y'])
		self.add_to_path(first)
		last=self.find_last_target_tile(conf['x'],conf['y'])
		self.add_to_path(last)
		
	def path_target_reached(self,tile_target):
		self.start_marking()
		
class HSprinter(Sprinter):
	def __init__(self,player,conf):
		Sprinter.__init__(self,player,conf)		
		
	def get_confirmation_msg(self):
		'''property'''
		return {network.stc_new_unit:{'pid':self.owner.pid,
									  'eid':self.eid,
									  'type':'h_sprinter',
									  'tileid':self.tile.eid,
									  'move_speed':self.move_speed}}
	
	def find_first_target_tile(self,x,y):
		#choose right or left side
		if x>self.tile.x:
			return self.max_x_for_y_tile(y)
		else:
			return self.min_x_for_y_tile(y)

	def find_last_target_tile(self,x,y):
		#then go to the other side
		if x>self.tile.x:
			return self.min_x_for_y_tile(y)
		else:
			return self.max_x_for_y_tile(y)
		
	confirmation_msg=property(get_confirmation_msg)
	

class VSprinter(Sprinter):
	def __init__(self,player,conf):
		Sprinter.__init__(self,player,conf)
		
	def get_confirmation_msg(self):
		'''property'''
		return {network.stc_new_unit:{'pid':self.owner.pid,
									  'eid':self.eid,
									  'type':'v_sprinter',
									  'tileid':self.tile.eid,
									  'move_speed':self.move_speed}}

	def find_first_target_tile(self,x,y):
		return self.min_y_for_x_tile(x)

	def find_last_target_tile(self,x,y):
		return self.max_y_for_x_tile(x)

	confirmation_msg=property(get_confirmation_msg)

