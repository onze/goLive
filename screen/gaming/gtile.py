
from panda3d.core import TextureStage,TransparencyAttrib

from screen.gaming.gentity import GEntity

class GTile(GEntity):
	
	def __init__(self,conf):
		self.p3dobject=self.gmap.tile_matrix_node.attachNewNode('tile_'+str(conf['eid']))
		self.p3dobject.setTransparency(TransparencyAttrib.MAlpha)
		#self.test_sphere=loader.loadModel('data/models/test_sphere.egg')
		#self.test_sphere.reparentTo(self.p3dobject)
		GEntity.__init__(self,conf)
		self.x,self.y=x,y=conf['x'],conf['y']
		self.p3dobject.setTag('x',str(x))
		self.p3dobject.setTag('y',str(y))
		#half of a tile side
		t=self.gmap.tile_matrix_node.getScale()[0]/2.
		self.p3dobject.setPos(self.gmap.tile_matrix_node,(-self.gmap.resx/2.+x+t)*2.,(y-self.gmap.resy/2.+t)*2.,0)
		
		#preload texture holder quad
		self.quad=GTile.resources['quad']()
		self.quad.setTransparency(TransparencyAttrib.MAlpha)
		self.quad.reparentTo(self.p3dobject)
		self.quad.hide()
		
		#load_level
		self.ts_load_level=TextureStage('ts_load_level')
		self.ts_load_level.setMode(TextureStage.MReplace)
		self.ts_load_level.setSort(1)
		
		self.pawner=None
		#owner
		self.ts_pawn=TextureStage('ts_pawn')
		self.ts_pawn.setMode(TextureStage.MDecal)
		self.ts_pawn.setSort(2)
		
		#selection
		self.is_selected=False
		self.ts_selected=TextureStage('ts_selected')
		self.ts_selected.setMode(TextureStage.MReplace)
		self.ts_selected.setSort(3)
		
		#highlight
		self.is_highlighted=False
		self.ts_highlighted=TextureStage('ts_highlighted')
		self.ts_highlighted.setMode(TextureStage.MDecal)
		self.ts_highlighted.setSort(4)
	
	@staticmethod
	def load_resources():
		#dict of texture
		GTile.resources={'quad':lambda:loader.loadModel('data/models/tiles/tile.egg')}
		GTile.textures={'highlighted':loader.loadTexture('data/models/tiles/tile.highlighted.tex.png'),
					   	'selected':loader.loadTexture('data/models/tiles/tile.selected.tex.png'),
					   	'pawn-black':loader.loadTexture('data/models/tiles/tile.pawned.black.tex.png'),
					   	'pawn-white':loader.loadTexture('data/models/tiles/tile.pawned.white.tex.png'),
					   	'black-load_level-1':loader.loadTexture('data/models/tiles/tile.owned.black.1.tex.png'),
					   	'black-load_level-3':loader.loadTexture('data/models/tiles/tile.owned.black.3.tex.png'),
					   	'white-load_level-1':loader.loadTexture('data/models/tiles/tile.owned.white.1.tex.png'),
					   	'white-load_level-3':loader.loadTexture('data/models/tiles/tile.owned.white.3.tex.png'),
				       }
	
	def change_load_level(self,data):
		'''
		shown levels are level 0, 1 and 3, respectively neutral, half filled and fully filled tile
		'''
		out('tile '+str(self.eid)+'\'s load_level set to '+str(data))
		self.load_level=data['level']
		self.owner=data['owner']
		if self.load_level==0:
			self.quad.clearTexture(self.ts_load_level)
		else:
			color={0:'black',1:'white'}[self.owner]
			self.quad.setTexture(self.ts_load_level,self.textures[color+'-load_level-'+str(self.load_level)])
			self.quad.show()

	def change_pawner(self,data):
		#out('tile '+str(self.eid)+' set to '+str(data['owner']))
		self.pawner=data['pawner']
		if self.pawner==None:
			self.quad.clearTexture(self.ts_pawn)
			if not (self.is_selected or self.is_highlighted or self.owner!=None):
				self.quad.hide()
		else: 
			color={0:'black',1:'white'}[self.pawner]
			self.quad.setTexture(self.ts_pawn,self.textures['pawn-'+color])
			self.quad.show()		
	
	def set_highlighted(self):
		#out('tile.eid='+str(self.eid))
		self.is_highlighted=True
		self.quad.show()
		self.quad.setTexture(self.ts_highlighted,self.textures['highlighted'])
	
	def unset_highlighted(self):
		self.is_highlighted=False
		self.quad.clearTexture(self.ts_highlighted)
		if not (self.is_selected or self.pawner!=None):
			self.quad.hide()
	
	def set_selected(self):
		self.is_selected=True
		self.quad.show()
		self.quad.setTexture(self.ts_selected,self.textures['selected'])
	
	def unset_selected(self):
		self.is_selected=False
		self.quad.clearTexture(self.ts_selected)
		if not (self.is_highlighted or self.pawner!=None):
			self.quad.hide()

	@property
	def center_pos(self):
		return self.p3dobject.getPos()

		