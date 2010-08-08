
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
		
		#pid of the player that owns the tile
		self.pawner=None
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
		
	def __repr__(self):
		return 'GTile{eid:'+str(self.eid)+'\n\
x/y:'+str(self.x)+'/'+str(self.y)+'\n\
pawner:'+str(self.pawner)+'\n\
selected:'+str(self.is_selected)+'\n\
highlighted:'+str(self.is_highlighted)+'\n\
}'
	
	def __str__(self):
		return self.__repr__()
	
	@staticmethod
	def load_resources():
		#dict of texture
		GTile.resources={	'quad':lambda:loader.loadModel('data/models/tiles/tile.egg'),
								}
		GTile.textures={	'highlighted':loader.loadTexture('data/models/tiles/tile.highlighted.tex.png'),
					   		'selected':loader.loadTexture('data/models/tiles/tile.selected.tex.png'),
					   		'pawn-black':loader.loadTexture('data/models/tiles/tile.pawned.black.tex.png'),
					   		'pawn-white':loader.loadTexture('data/models/tiles/tile.pawned.white.tex.png'),
				       		}

	@property
	def left_tile(self):
		'''property getter'''
		if self.x>0:return self.gmap.tile_matrix[self.x-1][self.y]
		return None

	@property
	def lower_tile(self):
		'''property getter'''
		if self.y>0:return self.gmap.tile_matrix[self.x][self.y-1]
		return None

	@property
	def right_tile(self):
		'''property getter'''
		if self.x<self.gmap.resx-1:return self.gmap.tile_matrix[self.x+1][self.y]
		return None

	@property
	def upper_tile(self):
		'''property getter'''
		if self.y<self.gmap.resy-1:return self.gmap.tile_matrix[self.x][self.y+1]
		return None

	@property
	def neighbors(self):
		'''property getter'''
		return filter(lambda t:t!=None,[self.left_tile,self.lower_tile,self.right_tile,self.upper_tile])

	@property
	def wall(self):
		'''
		returns a list of all tiles that form a wall connected to this tile.
		a tile with no pawner doesn't belong to any wall.
		'''
		if self.pawner==None:
			return []
		wall=[]
		fringe=[self]
		visited={}
		while len(fringe):
			t=fringe.pop(0)
			if t.pawner==self.pawner:
				wall.append(t)
				visited[t]=1
			fringe.extend([n for n in t.neighbors if n.pawner==self.pawner and n not in visited])

	def change_pawner(self,data):
		#out('tile '+str(self.eid)+' set to '+str(data['owner']))
		if self.pawner!=data['pawner']:
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


		