
from unit import Unit

class TileMarker(Unit):
	'''
	inherited by classes of objets that needs to mark tiles on their path (non fighter units).
	'''
	def __init__(self,player):
		Unit.__init__(self,player)
		
	def on_tile_change(self):
		if not self.current_tile.pawner:
			self.current_tile.pawner=self.owner
			self.current_tile.owner=self.owner
			self.current_tile.load_level=3