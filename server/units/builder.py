
from unit import Unit

class Builder(Unit):
	'''
	inherited by units that needs to build on tiles they pass by (non fighter units).
	'''
	def __init__(self,player):
		Unit.__init__(self,player)
		
	def on_tile_change(self):
		if self.current_tile.pawner==None:
			#TODO: sendevent to GUnit for special animation ?
			#out('Tilemarker.on_tile_change: tile ',self.current_tile.eid, 'set from pawner',self.current_tile.pawner,' to ',self.owner.pid)
			self.current_tile.pawner=self.owner