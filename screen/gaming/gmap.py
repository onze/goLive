
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from pandac.PandaModules import NodePath,RigidBodyCombiner

from screen.gaming.gamingcam import GamingCam
#from ..widgetwrappers import WidgetWrapper
from screen.gaming.gentity import GEntity
from screen.gaming.gtile import GTile
from screen.gaming.gunit import GV_Sprinter,GH_Sprinter
from screen.gaming.gtilequadtree import GTileQuadTree
from screen.widget import Widget
import tools

class GMap(Widget,DirectObject):
   '''
   responsible for anything on the game board as well as the board itself, as well as the camera.
   the grid of tiles is a single model with a texture of tiles, and a matrix a GTiles.
   '''
   def __init__(self,*args,**kwargs):
      DirectObject.__init__(self)
      Widget.__init__(self,*args,**kwargs)
      #root of anything on the board
      self.root=base.render.attachNewNode('GMap.root')
      self.gcam=GamingCam(self,tools.Rectangle(self.x,self.y,self.w,self.h))
      self.gcam.level=.7
      self.gcam.target=(0,-9,0)
      #node containing GTiles' quads (textures)      
      self.tiles_quads_node=self.root.attachNewNode('GMap.tile_quads_node')
      #node containing every GUnits      
      self.units_node=self.root.attachNewNode('GMap.units_node')
      #tile selection stuff
      self.is_tile_selection_enabled=False
      self.selected_tiles=[]
      self.highlighted_tiles=[]
      #unit selection stuff
      #gunits are saved (not only their models)
      self.selected_unit=None
      self.highlighted_unit=None
      self.is_unit_selection_enabled=False
      GEntity.gmap=GTileQuadTree.map=self
      

   def __del__(self):
      del self.gcam
      self.root.destroy()
      self.tile_matrix_node.destroy()
      #TODO: unload ressources ?

   @staticmethod
   def load_resources():
      GTile.load_resources()
      #simple models dict
      GMap.model_res={  'tile_matrix_xs':loader.loadModel('data/models/tiles/tile_matrix_xs.egg'),
                        'tile_matrix_s':loader.loadModel('data/models/tiles/tile_matrix_s.egg'),
                        'tile_matrix_m':loader.loadModel('data/models/tiles/tile_matrix_m.egg'),
                   }
      #dict{id:{model:'file path',animations{'name':'file path'}},etc}
      #models are stored alone in their egg file
      #each animation is also stored in its own egg file
      GMap.actor_res={'home':{  'model':'data/models/buildings/home.egg',
                          'animations':{'anim':'data/models/buildings/home-anim.egg'}
                        },
                   }

   def build_tile_matrix(self,res,resx,resy):
      '''
      builds the playing grid, that is a resx*resy matrix of tiles.
      '''
      #every tile nodes will be attached to this one
      self.tile_matrix_node=self.model_res['tile_matrix_'+res]
      self.tile_matrix_node.reparentTo(self.root)
      #self.tile_matrix_origin_np=self.tile_matrix_node.attachNewNode('tile_matrix_origin')
      #self.tile_matrix_origin_np.setPos(-resx,-resy,0)
      self.tile_matrix=[[None for _ in range(resy)] for _ in range(resx)]

   def enable_tile_highlight(self,mode):
      '''
      hovered tiles will be colored depending on the given mode ('column', 'row', 'single')
      '''
      out('gmap.enable_tile_highlight(mode='+mode+')')
      self.highlight_mode=mode
      self.highlighted_tiles=[]
      update_list.append(self.update_highlighted_tiles)

   def disable_tile_highlight(self):
      out('gmap.disable_tile_highlight()')
      self.highlight_mode=None
      [tile.unset_highlighted() for tile in self.highlighted_tiles]
      self.highlighted_tiles=[]
      if self.update_highlighted_tiles in update_list: 
         update_list.remove(self.update_highlighted_tiles)
      
   def update_highlighted_tiles(self):
      '''
      called every frame when tile highlighting is enabled.
      does the real job.
      '''
      old=list(self.highlighted_tiles)
      if self.highlight_mode==None:
         return
      elif self.highlight_mode=='column':
         picked=self.gcam.get_picked_tile()
         if picked:
            self.highlighted_tiles=[]#get all tiles with this x from tile_matrix
         else:
            self.highlighted_tiles=[]
      elif self.highlight_mode=='row':
         picked=self.gcam.self.gcam.get_picked_tile()
         if picked:
            self.highlighted_tiles=[]#get all tiles with this y from tile_matrix
         else:
            self.highlighted_tiles=[]
      elif self.highlight_mode=='single':
         picked=self.gcam.get_picked_tile()
         if picked:
            self.highlighted_tiles=[picked]
         else:
            self.highlighted_tiles=[]
      elif self.highlight_mode in ['allied-wall','enemy-wall']:
         picked=self.gcam.get_picked_tile()
         if picked:
            if self.highlight_mode=='allied-wall' and picked.pawner==screen.frame.pid:
               self.highlighted_tiles=picked.wall
            elif self.highlight_mode=='enemy-wall' and picked.pawner!=screen.frame.pid:
               self.highlighted_tiles=picked.wall
            else:
               self.highlighted_tiles=[]
         else:
            self.highlighted_tiles=[]
      if self.highlighted_tiles!=old:
         [tile.unset_highlighted() for tile in old]
         [tile.set_highlighted() for tile in self.highlighted_tiles]

   def enable_tile_selection(self,mode):
      '''
      will keep track of hovered tiles depending on the given mode ('column','row','single','allied-wall','enemy-wall'),
      storing a list of them into self.selected_tiles. 
      '''
      out('gmap.enable_tile_selection(mode='+mode+')')
      self.is_tile_selection_enabled=True
      #self.gcam.push_state()
      #self.gcam.center()
      #self.gcam.disable_move()
      #self.gcam.level=1
      self.enable_tile_highlight(mode)
      self.selected_tiles=[]
      self.accept('mouse1-up',self.set_selected_tiles)
      
   def disable_tile_selection(self):
      '''disabling the selection deletes the selection'''
      out('gmap.disable_tile_selection()')
      self.ignore('mouse1-up')
      self.is_tile_selection_enabled=False
      #self.gcam.enable_move()
      #self.gcam.pop_state()
      self.disable_tile_highlight()
      [tile.unset_selected() for tile in self.selected_tiles]
      self.selected_tiles=[]      
      
   def set_selected_tiles(self):
      '''
      called at left mouse click when tile selection is enabled.
      '''
      [tile.unset_selected() for tile in self.selected_tiles]
      self.selected_tiles=list(self.highlighted_tiles)
      for tile in self.selected_tiles:
         tile.set_selected()
      
   def enable_unit_highlight(self,mode):
      out('gmap.enable_unit_highlight(mode='+mode+')')
      self.highlight_mode=mode
      self.highlighted_unit=None
      update_list.append(self.update_highlighted_unit)
      
   def disable_unit_highlight(self):
      self.highlighted_unit=None
      
   def update_highlighted_unit(self):
      '''
      called every frame when unit highlighting is enabled.
      '''
      old=self.highlighted_unit
      self.highlighted_unit=None
      if self.highlight_mode==None:
         return
      else:
         picked=self.gcam.get_picked_unit()
         if picked:
            picked=picked.getPythonTag('ref')
            if self.highlight_mode=='ennemy' and picked.pid!=screen.frame.pid:
               self.highlighted_unit=picked
            if self.highlight_mode=='ally' and picked.pid==screen.frame.pid:
               self.highlighted_unit=picked
      if self.highlighted_unit:
         if self.highlighted_unit!=old:
            if old:
               old.unset_highlighted()
            if self.highlighted_unit:
               self.highlighted_unit.set_highlighted()
      elif old:
            old.unset_highlighted()
      
   def enable_unit_selection(self,mode):
      '''
      mode can be one of the following: 'ally', 'ennemy'
      '''
      out('GMap.enable_unit_selection')
      self.is_unit_selection_enabled=True
      self.gcam.push_state()
      self.gcam.center()
      self.gcam.disable_move()
      self.gcam.level=1
      self.enable_unit_highlight(mode)
      self.selected_unit=None
      self.accept('mouse1-up',self.set_selected_unit)
      
   def disable_unit_selection(self):
      out('GMap.disable_unit_selection')
      self.is_unit_selection_enabled=False
      self.gcam.enable_move()
      self.gcam.pop_state()
      self.ignore('mouse1-up')
      self.disable_unit_highlight()
      if self.selected_unit:
         self.selected_unit.unset_selected()
         self.selected_unit=None
      
   def set_selected_unit(self):
      '''
      called at left mouse click when unit selection is enabled.
      '''
      if self.selected_unit:
         self.selected_unit.unset_selected()
      self.selected_unit=self.highlighted_unit
      if self.selected_unit:
         self.selected_unit.set_selected()
         
   def start_accepting(self):
      '''
      start accepting user mouse/keyboard input.
      '''
      self.tiles_quads_node.flattenStrong()
      self.gcam.start_accepting()

   def new_home(self,data):
      #http://www.panda3d.org/wiki/index.php/Loading_Actors_and_Animations
      home=Actor(self.actor_res['home']['model'],self.actor_res['home']['animations'])
      home.loop('anim')
      home.reparentTo(self.root)
      home.setPythonTag('eid',data['eid'])
      target=self.tile_matrix_node.find('**/tile_'+str(data['tileid']))
      home.setPos(target,0,0,0)
      GEntity.instances[data['eid']]=home
      out('GMap.new_home: data='+str(data))
      '''
      #way to get a tile node's pos back after the tile matrix flattening
      target=self.root.find('**/tile_'+str(data['tileid'])).getPythonTag('ref')
      t=self.tile_matrix_node.getScale()[0]/2.
      home.setPos(self.tile_matrix_node,(-self.resx/2.+target.x+t)*2.,(target.y-self.resy/2.+t)*2.,0)
      '''

   def new_tile(self,data):
      '''
      synchronizes a tile on the server with its mirror here.
      '''
      gtile=GTile(data)
      self.tile_matrix[data['x']][data['y']]=gtile
      #self.tile_quadtree.add(data['x'],data['y'],gtile)

   def new_unit(self,conf):
      '''
      instanciates a unit on the map.
      '''
      switch={'v_sprinter':GV_Sprinter,
             'h_sprinter':GH_Sprinter,
             }
      switch[conf['type']](conf)

   @property
   def resx(self):
      return len(self.tile_matrix)

   @property
   def resy(self):
      if len(self.tile_matrix)>0:
         return len(self.tile_matrix[0])
      return 0
