
from panda3d.core import Vec4,TextureStage,TransparencyAttrib

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
		
		self.pawner=None
		#owner white
		self.ts_pawn_white=TextureStage('ts_pawn_white')
		self.ts_pawn_white.setMode(TextureStage.MReplace)
		self.ts_pawn_white.setSort(1)
		
		#owner black
		self.ts_pawn_black=TextureStage('ts_pawn_black')
		self.ts_pawn_black.setMode(TextureStage.MReplace)
		self.ts_pawn_black.setSort(1)
		
		#selection
		self.is_selected=False
		self.ts_selected=TextureStage('ts_selected')
		self.ts_selected.setMode(TextureStage.MReplace)
		self.ts_selected.setSort(2)
		
		#highlight
		self.is_highlighted=False
		self.ts_highlighted=TextureStage('ts_highlighted')
		self.ts_highlighted.setMode(TextureStage.MDecal)
		self.ts_highlighted.setSort(3)
	
	@staticmethod
	def load_resources():
		#dict of texture
		GTile.resources={'quad':lambda:loader.loadModel('data/models/tile.egg')}
		GTile.textures={'highlighted':loader.loadTexture('data/models/tile.highlighted.tex.png'),
					   	'selected':loader.loadTexture('data/models/tile.selected.tex.png'),
					   	'pawn-black':loader.loadTexture('data/models/tile.pawned.black.tex.png'),
					   	'pawn-white':loader.loadTexture('data/models/tile.pawned.white.tex.png')
				       }
		
	def change_pawner(self,data):
		#out('tile '+str(self.eid)+' set to '+str(data['owner']))
		self.pawner=data['pawner']
		if self.pawner==0:
			self.quad.setTexture(self.ts_pawn_black,self.textures['pawn-black'])
		else:
			self.quad.setTexture(self.ts_pawn_white,self.textures['pawn-white'])
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

		