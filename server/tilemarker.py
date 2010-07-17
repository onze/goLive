
from unit import Unit

class TileMarker(Unit):
	'''
	inherited by classes of objets that needs to mark tiles on their path (non fighter units).
	'''
	def __init__(self,player):
		Unit.__init__(self,player)
		
	def on_tile_change(self):
		if self.current_tile.pawner==None:
			#TODO: sendevent to GUnit for special animation ?
			self.current_tile.pawner=self.owner
			self.current_tile.load_level=3