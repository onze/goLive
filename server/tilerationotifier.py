
import network
import player
import tile

class TileRatioNotifier:
   '''
   keeps clients in sync with tile ratio.
   updates are triggered by tiles on owner change.
   '''
   def __init__(self,server):
      self.server=server
      self.ratio={None:len(tile.Tile.instances[tile.Tile.eitype])}
      for pid in player.Player.instances:
         self.ratio[pid]=0
      self.has_changed=False
      tile.Tile.ratio_notifier=self
      
   def update_ratio(self,old,new):
      '''
      called by a tile when it changes owner
      '''
      self.ratio[old]-=1
      self.ratio[new]+=1
      self.has_changed=True
      
   def update(self):
      '''called once a frame to sync clients if needed'''
      if self.has_changed:
         self.server.send({network.stc_tile_ratio_change:{'ratio':dict(self.ratio)}})
         self.has_changed=False
      
      
      