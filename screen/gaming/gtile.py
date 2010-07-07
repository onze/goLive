
from panda3d.core import Vec4, TextureStage

from gentity import GEntity

class GTile(GEntity):
	
	def __init__(self,conf):
		self.p3dobject=self.gmap.tile_matrix_node.attachNewNode('tile_'+str(conf['eid']))
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
		self.quad=GTile.resources['model']()
		self.quad.reparentTo(self.p3dobject)
		self.quad.hide()
		
		#highlight
		self.is_highlighted=False
		self.ts_highlighted=TextureStage('ts_highlighted')
		self.ts_highlighted.setMode(TextureStage.MDecal)
		self.ts_highlighted.setSort(1)
		
		#selection
		self.is_selected=False
		self.ts_selected=TextureStage('ts_selected')
		self.ts_selected.setMode(TextureStage.MDecal)
		self.ts_selected.setSort(2)
	
	@staticmethod
	def load_resources():
		#dict of texture
		GTile.resources={'model':lambda:loader.loadModel('data/models/tile.egg')}
		GTile.textures={'highlighted':lambda:loader.loadTexture('data/models/tile.highlighted.tex.png'),
					   	'selected':lambda:loader.loadTexture('data/models/tile.selected.tex.png'),
				       }
		
	def change_owner(self,data):
		self.owner=data['owner']
		#TODO: change color
	
	def set_highlighted(self):
		#out('tile.eid='+str(self.eid))
		self.is_highlighted=True
		self.quad.show()
		self.quad.setTexture(self.ts_highlighted,self.textures['highlighted']())
	
	def unset_highlighted(self):
		self.is_highlighted=False
		#self.quad.clearTexture(self.ts_highlighted)
		if not self.is_selected:
			self.quad.hide()
	
	def set_selected(self):
		self.is_selected=True
		self.quad.show()
		self.quad.setTexture(self.ts_selected,self.textures['selected']())
	
	def unset_selected(self):
		self.is_selected=False
		self.quad.clearTexture(self.ts_selected)
		if not self.is_highlighted:
			self.quad.hide()

	@property
	def center_pos(self):
		return self.p3dobject.getPos()

		