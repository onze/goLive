
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from panda3d.core import Vec4
#from pandac.PandaModules import RigidBodyCombiner,NodePath

from gamingcam import GamingCam
#from ..widgetwrappers import WidgetWrapper
from gentity import GEntity
from gtile import GTile
from gunit import GV_Sprinter,GH_Sprinter
from ..widget import Widget
from tools import random
from ..server import network
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
		self.gcam.level=.5
		self.gcam.target=self.root
		self.selected_tiles=[]
		self.highlighted_tiles=[]
		self.is_tile_selection_enabled=False
		GEntity.gmap=self
		

	def __del__(self):
		del self.gcam
		self.root.destroy()
		self.tile_matrix_node.destroy()
		#TODO: unload ressources ?

	@staticmethod
	def load_resources():
		GTile.load_resources()
		#simple models dict
		GMap.model_res={'tile_matrix_xs':loader.loadModel('data/models/tile_matrix_xs.egg'),
					    'tile_matrix_m':loader.loadModel('data/models/tile_matrix_m.egg')}
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
		#every nodes will be attached to this one
		self.tile_matrix_node=self.model_res['tile_matrix_'+res]
		self.tile_matrix_node.reparentTo(self.root)
		#self.tile_matrix_origin_np=self.tile_matrix_node.attachNewNode('tile_matrix_origin')
		#self.tile_matrix_origin_np.setPos(-resx,-resy,0)
		self.tile_matrix=[[None for y in range(resy)] for x in range(resx)]

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
		#if len(self.highlighted_tiles) and self.highlighted_tiles[0] in self.selected_tiles:
		#	self.color_tiles(self.highlighted_tiles,self.selected_tiles_color)
		#else:
		#	self.color_tiles(self.highlighted_tiles,self.normal_tiles_color)
		old=list(self.highlighted_tiles)
		if self.highlight_mode==None:
			return
		elif self.highlight_mode=='column':
			picked=self.gcam.get_picked_tile()
			if picked==None:return
			self.highlighted_tiles=self.tile_matrix_node.findAllMatches('**/=x='+str(picked.x))
		elif self.highlight_mode=='row':
			picked=self.gcam.self.gcam.get_picked_tile()
			if picked==None:return
			self.highlighted_tiles=self.tile_matrix_node.findAllMatches('**/=y='+str(picked.y))
		elif self.highlight_mode=='single':
			picked=self.gcam.get_picked_tile()
			if picked==None:return
			self.highlighted_tiles=[picked]
		if self.highlighted_tiles!=old:
			[tile.unset_highlighted() for tile in old]
			[tile.set_highlighted() for tile in self.highlighted_tiles]

	def enable_tile_selection(self,mode):
		'''
		will keep track of hovered tiles depending on the given mode ('column','row','single'),
		storing a list of them into self.selected_tiles. 
		'''
		out('gmap.enable_tile_selection()')
		self.is_tile_selection_enabled=True
		self.gcam.push_state()
		self.gcam.center()
		self.gcam.disable_move()
		self.gcam.level=1
		self.enable_tile_highlight(mode)
		self.selected_tiles=[]
		self.accept('mouse1-up',self.set_selected_tiles)
		
	def disable_tile_selection(self):
		'''disabling the selection deletes the selection'''
		out('gmap.disable_tile_selection()')
		self.ignore('mouse1-up')
		self.is_tile_selection_enabled=False
		self.gcam.enable_move()
		self.gcam.pop_state()
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

	def new_home(self,data):
		#http://www.panda3d.org/wiki/index.php/Loading_Actors_and_Animations
		home=Actor(self.actor_res['home']['model'],self.actor_res['home']['animations'])
		home.loop('anim')
		home.reparentTo(self.root)
		home.setPythonTag('eid',data['eid'])
		home.setPos(self.root.find('**/tile_'+str(data['tileid'])),0,0,0)
		GEntity.instances[data['eid']]=home
		out('GMap.new_home: data='+str(data))
		#out(scale=tile.getScale(),y=(y-resy/2.)*2.*s)

	def new_tile(self,data):
		'''
		synchronizes a tile on the server with its mirror here.
		'''
		self.tile_matrix[data['x']][data['y']]=GTile(data)

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





